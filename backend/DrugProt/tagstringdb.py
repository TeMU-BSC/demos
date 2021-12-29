import os
import sys
import re

import numpy as np
import spacy

from collections import deque
from collections import namedtuple
import functools
from multiprocessing import Pool
from multiprocessing import cpu_count
import tensorflow as tf
#from tensorflow.keras import backend as K

from common import load_ner_model, process_sentences, encode, argument_parser, get_predictions
from biocreativedb import stream_documents
import datetime


# Alnum sequences preserved as single tokens, rest are
# single-character tokens.
TOKENIZATION_RE = re.compile(r'([^\W_]+|.)')

BcrDoc = namedtuple(
    'BcrDoc',
    'doc_id, text, tids, sids, data'
)


def sentence_split_old(text):
    if sentence_split.nlp is None:
        # Cache spacy model
        nlp = spacy.load('en_core_sci_sm', disable=['tagger', 'ner','pos'])
        nlp.add_pipe('sentencizer')
        sentence_split.nlp = nlp
    return [s.text for s in sentence_split.nlp(text).sents]
#sentence_split.nlp = None

def sentence_split(text):
    if sentence_split.nlp is None:
        # Cache spacy model                                                     
        nlp = spacy.load('en_core_sci_sm', disable=['tagger','parser','ner','lemmatizer','textcat','pos'])
        nlp.add_pipe('sentencizer')
        sentence_split.nlp = nlp
    sentence_texts = []
    for para in text.split('\t'):
        sentence_texts.extend([s.text for s in sentence_split.nlp(para).sents])
    return sentence_texts
sentence_split.nlp = None

def tokenize(text):
    return [t for t in TOKENIZATION_RE.split(text) if t and not t.isspace()]


def split_and_tokenize(text):
    sentences = sentence_split(text)
    return [tokenize(s) for s in sentences]


def dummy_labels(tokenized_sentences):
    sentence_labels = []
    for tokens in tokenized_sentences:
        sentence_labels.append(['O'] * len(tokens))
    return sentence_labels


def get_word_labels(orig_words, token_lengths, tokens, predictions):
    """Map wordpiece token labels to word labels."""
    toks = deque([val for sublist in tokens for val in sublist])
    pred = deque([val for sublist in predictions for val in sublist])
    lengths = deque(token_lengths)
    word_labels = []
    for sent_words in orig_words:
        sent_labels = []
        for word in sent_words:
            sent_labels.append(pred.popleft())
            for i in range(int(lengths.popleft())-1):
                pred.popleft()
        word_labels.append(sent_labels)
    return word_labels


def iob2_span_ends(curr_type, tag):
    if curr_type is None:
        return False
    elif tag == 'I-{}'.format(curr_type):
        return False
    elif tag == 'O' or tag[0] == 'B':
        return True
    else:
        assert curr_type != tag[2:], 'internal error'
        return True    # non-IOB2 or tag sequence error


def iob2_span_starts(curr_type, tag):
    if tag == 'O':
        return False
    elif tag[0] == 'B':
        return True
    elif curr_type is None:
        return True    # non-IOB2 or tag sequence error
    else:
        assert tag == 'I-{}'.format(curr_type), 'internal error'
        return False


def tags_to_spans(text, tokens, tags):
    spans = []
    offset, curr_type, start = 0, None, None
    assert len(tokens) == len(tags)
    for token, tag in zip(tokens, tags):
        if iob2_span_ends(curr_type, tag):
            spans.append((start, offset, curr_type, text[start:offset]))
            curr_type, start = None, None
        while offset < len(text) and text[offset].isspace():
            offset += 1
        if text[offset:offset+len(token)] != token:
            raise ValueError('text mismatch')
        if iob2_span_starts(curr_type, tag):
            curr_type, start = tag[2:], offset
        offset += len(token)
    if curr_type is not None:
        spans.append((start, offset, curr_type, text[start:offset]))
    return spans

def write_sentences(outfile, sentences, labels):
    for sentence, tagseq in zip(sentences,labels):
        for word, tag in zip(sentence, tagseq):
            outfile.write('{}\t{}\n'.format(word, tag))
        outfile.write('\n')

def writespans(infile, doc_id, spans):
    for i,s in enumerate(spans):
        infile.write('{}\tT{}\t{}\t{}\t{}\t{}\n'.format(doc_id,i+1,s[2],s[0],s[1],s[3]))



def create_samples(tokenizer, seq_len, document):
    words = split_and_tokenize(document.text)
    labels = dummy_labels(words)
    data = process_sentences(words, labels, tokenizer, seq_len) #One doc at time --> documentwise
    tids, sids = encode(data.combined_tokens, tokenizer, seq_len)
    return BcrDoc(document.doc_id, document.text, tids, sids, data)    


def main(argv):
    #tf.keras.backend.clear_session()
    #tf.config.optimizer.set_jit(True) 
    #tf.config.optimizer.set_jit(True)
    argparser = argument_parser()
    args = argparser.parse_args(argv[1:])

    infn = args.train_data
    #if infn[-12:-4]=='part-001':
    #    exit()
    outfn = './biocreative-output/{}-spans.tsv'.format(args.output_file)
    out_tsv = './biocreative-output/{}-sentences.tsv'.format(args.output_file)
    ner_model, tokenizer, labels, config = load_ner_model(args.ner_model_dir)
    
    #@tf.function
    #def nerm(data):
    #    return ner_model(data)
    
    #Set status for inference
    ner_model.trainable = False
    ner_model.training = False
    #ner_model.call = tf.function(ner_model.call) #, experimental_relax_shapes)
    #K.set_learning_phase(0)  #Force the inference status and discard 

    seq_len = config['max_seq_length']
    batch_size = args.batch_size

    tag_map = { l: i for i, l in enumerate(labels) }
    inv_tag_map = { v: k for k, v in tag_map.items() }

    # TODO take input path from argv

    #infn = '/scratch/project_2001426/stringdata/week_31_2-sample/database_documents.tsv'

    print("Preprocessing and inference starts: ", datetime.datetime.now(),flush=True)
    with open(outfn, 'w+') as of:
        
        #input_sentences=[]

        #num_input_sentences = 0
        #toks = np.array([], dtype=np.int64).reshape(0,seq_len)
        #seqs = np.array([], dtype=np.int64).reshape(0,seq_len)
        #toks = []
        #seqs = []
        #data_list = []
        print("CPU count ", cpu_count())
        partial_create_documents = functools.partial(create_samples,tokenizer,seq_len)
        with Pool(cpu_count()-1) as p:
            input_docs = p.map(partial_create_documents,stream_documents(infn))
            print("input docs len", len(input_docs), flush=True)

                
            input_sentences=[]
            num_input_sentences = 0
            #toks = np.array([], dtype=np.int64).reshape(0,seq_len)
            #seqs = np.array([], dtype=np.int64).reshape(0,seq_len)
            data_list = []
            tok_start = 0
            for count,document in enumerate(input_docs):

                #toks = np.concatenate((toks, document.tids))
                #seqs = np.concatenate((seqs, document.sids))
                num_input_sentences+=len(document.tids)
                data_list.append(document.data)
                input_sentences.append((document.doc_id, num_input_sentences, document.text))  #Sentences per doc for writing spans

                if num_input_sentences > args.sentences_on_batch:
                    print("num input sentences ", num_input_sentences)
                    print("Tok start ",tok_start)
                    print("count ", count)
                    toks = np.array([sample for samples in input_docs[tok_start:count+1] for sample in samples.tids])
                    seqs = np.array([sample for samples in input_docs[tok_start:count+1] for sample in samples.sids])
                    print("toks shape ", toks.shape)
                    print("seqs shape ", seqs.shape)
                    tok_start = count+1
                    print("Inference starts: ", datetime.datetime.now(),flush=True)
                    print(num_input_sentences, datetime.datetime.now(),flush=True)
                    #toks = np.array(input_docs[:count])
                    #print(toks[0].shape, seqs[0].shape, toks[1].shape, seqs[1].shape)
                    #tt = np.concatenate(toks) 
                    #uu = np.concatenate(seqs)
                    #print("tids: ", tt.shape)
                    #print("sids: ", uu.shape)
                    probs = ner_model.predict((toks, seqs),batch_size=batch_size)#, verbose=1, batch_size=batch_size)
                    #probs = ner_model((toks, seqs)) #probs = ner_model.predict((toks, seqs), verbose=1, batch_size=batch_size)
                    preds = np.argmax(probs, axis=-1)
                    #pr_ensemble, pr_test_first = get_predictions(preds, data.tokens, data.sentence_numbers)
                    #lines_ensemble, sentences_ensemble = write_result(
                    #'./output/tagger-out.tsv', data.words, data.lengths,
                    #data.tokens, data.labels, pr_ensemble, mode='predict')
                    start = 0
                    print("Postprocess starts: ", datetime.datetime.now(),flush=True)
                    for data, indices in zip(data_list, input_sentences):
                        token_labels=[]
                        for i, pred in enumerate(preds[start:indices[1]]):
                            token_labels.append([inv_tag_map[p] for p in pred[1:len(data.tokens[i])+1]])
                        start=indices[1]
                        word_labels = get_word_labels(
                            data.words, data.lengths, data.tokens, token_labels)

                        # Flatten and map to typed spans with offsets
                        with open(out_tsv,'a+') as outputfile:
                            write_sentences(outputfile, data.words, word_labels)

                        word_sequence = [w for s in data.words for w in s]
                        tag_sequence = [t for s in word_labels for t in s]
                        spans = tags_to_spans(indices[2], word_sequence, tag_sequence)
                        #
                        writespans(of, indices[0], spans)
                    input_sentences=[]
                    data_list =[]
                    num_input_sentences=0
                    #toks=[]
                    #seqs=[]
                    toks = np.array([], dtype=np.int64).reshape(0,seq_len)
                    seqs = np.array([], dtype=np.int64).reshape(0,seq_len)
                    of.flush()
                    print("preprocess starts: ", datetime.datetime.now(),flush=True)

            if input_sentences:
                 
                toks = np.array([sample for samples in input_docs[tok_start:] for sample in samples.tids])
                seqs = np.array([sample for samples in input_docs[tok_start:] for sample in samples.sids])
                print("Inference starts: ", datetime.datetime.now(),flush=True)
                print(num_input_sentences, datetime.datetime.now(),flush=True)
                #dataset = tf.data.Dataset.from_tensor_slices((toks, seqs))
                #print(num_input_sentences, datetime.datetime.now(),flush=True)
                #print(toks[0].shape, seqs[0].shape, toks[1].shape, seqs[1].shape)
                #tt = np.concatenate(toks) 
                #uu = np.concatenate(seqs)
                #print("tids: ", tt.shape)
                #print("sids: ", uu.shape)
                probs = ner_model.predict((toks, seqs),batch_size=batch_size)#, verbose=1, batch_size=batch_size)
                #probs = nerm((tf.constant(toks),tf.constant(seqs)))
                #print("probs")
                preds = np.argmax(probs, axis=-1)
                #outdata = [item for data in data_list for item in data]
                #pr_ensemble, pr_test_first = get_predictions(preds, outdata.tokens, outdata.sentence_numbers)
                #lines_ensemble, sentences_ensemble = write_result(
                #'./output/tagger-out.tsv', data.words, data.lengths,
                #data.tokens, data.labels, pr_ensemble, mode='predict')
                start = 0
                for data, indices in zip(data_list, input_sentences):
                    #print(start)
                    token_labels=[]
                    for i, pred in enumerate(preds[start:indices[1]]):
                        token_labels.append([inv_tag_map[p] for p in pred[1:len(data.tokens[i])+1]])
                    start=indices[1]
                    word_labels = get_word_labels(
                        data.words, data.lengths, data.tokens, token_labels)
                    with open(out_tsv,'a+') as outputfile:
                        write_sentences(outputfile, data.words, word_labels)

                    # Flatten and map to typed spans with offsets
                    word_sequence = [w for s in data.words for w in s]
                    tag_sequence = [t for s in word_labels for t in s]
                    spans = tags_to_spans(indices[2], word_sequence, tag_sequence)
                    #
                    writespans(of, indices[0], spans)
    print("inference ends: ", datetime.datetime.now(),flush=True)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
