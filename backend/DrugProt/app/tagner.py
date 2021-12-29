import os
import sys
import unicodedata
from flask_cors import CORS
from flask import Flask, request
from app import app
import numpy as np
import tensorflow as tf
from flask import g, json, request, jsonify

from common import process_sentences, load_ner_model
from common import encode, write_result
from common import argument_parser

import re
import spacy

from collections import deque
from collections import namedtuple
from NER_utils.conll_to_brat import conll_to_brat, output_brat
from NER_utils.so2html import conll_to_standoff, standoff_to_html, generate_legend
from NER_utils.so2html import sort_types

from common import load_ner_model, process_sentences, encode, argument_parser, get_predictions
#from biocreativedb import stream_documents
#import datetime

CORS(app)

TOKENIZATION_RE = re.compile(r'([^\W_]+|.)')




BcrDoc = namedtuple(
    'BcrDoc',
    'text, tids, sids, data'
)

#def sentence_split_old(text):
#    if sentence_split.nlp is None:
#        # Cache spacy model
#        nlp = spacy.load('en_core_sci_sm', disable=['tagger', 'ner','pos'])
#        nlp.add_pipe('sentencizer')
#        sentence_split.nlp = nlp
#    return [s.text for s in sentence_split.nlp(text).sents]
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
    return BcrDoc(document.text, tids, sids, data)



DEFAULT_MODEL_DIR_GENE = '/app/ner-model-gene'
DEFAULT_MODEL_DIR_CHEMICAL = '/app/ner-model-chemical'

# app = Flask(__name__)


@app.route('/get_annotations', methods=['POST'])
def tag():
    json_input = request.json
    text = json_input['INPUTTEXT'].rstrip()
    model = json_input['MODEL']
    print("tagging")
    if model == "chemical":
        return app.tagger_chemical.tag(text)
    elif model == "gene":
        return app.tagger_gene.tag(text)
    else:
        return "Model not found"
    
    # #tokenized = request.values.get('tokenized') in ('1', 'True', 'true')
    # return app.tagger.tag(text) #, tokenized)

@app.route('/')
def hello():
    return "Hello World!"



def reconstruct_brat(json_path, outpath, conll_file):
    """

    Parameters
    ----------
    json_path : string
        Path to input JSON data. I need to to find the path to the Brat folder that was created inside the preprocessing function.
    outpath : string
        Path to folder where I will create my output
    conll_file : string
        Path to .BIO file created in the previous step.
    Returns
    -------
    None.
    """
    # Darryl: inside the preprocessing function, I converted the input files from JSON into Brat format and store them.
    # Darryl: the function conll_to_brat() needs to look at those Brat format files.
    brat_original_folder_test = os.path.join(
        os.path.dirname(json_path), 'brat')

    # Darryl: Output folder where you want to store your Brat files
    brat_output_folder_test = outpath

    # Darryl: In our case, this is the same as path to .BIO file created in the previous step
    conll_output_filepath_test = conll_file

    conll_to_brat(conll_file, conll_output_filepath_test,
                  brat_original_folder_test, brat_output_folder_test, overwrite=True)



class Tagger(object):
    def __init__(self, model, tokenizer, labels, config):
        self.model = model
        self.tokenizer = tokenizer
        self.labels = labels
        self.config = config
        #self.session = None
        #self.graph = None

    def tag(self, text, tokenized=False):
        max_seq_len = self.config['max_seq_length']
        inv_label_map = { i: l for i, l in enumerate(self.labels) }
        if tokenized:
            words = text.split()    # whitespace tokenization
        else:
            words = tokenize(text)    # approximate BasicTokenizer
        dummy = ['O'] * len(words)
        data = process_sentences([words], [dummy], self.tokenizer, max_seq_len)
        x = encode(data.combined_tokens, self.tokenizer, max_seq_len)
        #if self.session is None or self.graph is None:
        probs = self.model.predict(x, batch_size=8)    # assume singlethreaded
        #else:
        #    with self.session.as_default():
        #        with self.graph.as_default():
        #            probs = self.model.predict(x, batch_size=8)
        preds = np.argmax(probs, axis=-1)
        pred_labels = []
        for i, pred in enumerate(preds):
            pred_labels.append([inv_label_map[t]
                                for t in pred[1:len(data.tokens[i])+1]])
        lines, _ = write_result(
            'output.tsv', data.words, data.lengths,
            data.tokens, data.labels, pred_labels, mode='predict'
        )
        
        annotations = conll_to_standoff(text,"".join(lines))
        anns = [a.to_dict(text) for a in annotations]
        return jsonify(anns)

    @classmethod
    def load(cls, model_dir):
        # session/graph for multithreading, see https://stackoverflow.com/a/54783311
        #session = tf.Session()
        #graph = tf.get_default_graph()
        #with graph.as_default():
        #    with session.as_default():
        print(model_dir)
        model, tokenizer, labels, config = load_ner_model(model_dir)
        model.trainable = False
        model.training = False
        tagger = cls(model, tokenizer, labels, config)
        #tagger.session = session
        #tagger.graph = graph
        return tagger


punct_chars = set([
    chr(i) for i in range(sys.maxunicode)
    if (unicodedata.category(chr(i)).startswith('P') or
        ((i >= 33 and i <= 47) or (i >= 58 and i <= 64) or
         (i >= 91 and i <= 96) or (i >= 123 and i <= 126)))
])

translation_table = str.maketrans({ c: ' '+c+' ' for c in punct_chars })


def tokenize(text):
    return text.translate(translation_table).split()

app.tagger_gene = Tagger.load(DEFAULT_MODEL_DIR_GENE)
app.tagger_chemical = Tagger.load(DEFAULT_MODEL_DIR_CHEMICAL)

# def main(argv):
#     argparser = argument_parser('serve')
#     args = argparser.parse_args(argv[1:])
#     if args.ner_model_dir is None:
#         args.ner_model_dir = DEFAULT_MODEL_DIR
#     app.tagger = Tagger.load(args.ner_model_dir)
#     app.run(port=args.port,host='0.0.0.0')
#     return 0






# if __name__ == '__main__':
#     sys.exit(main(sys.argv))