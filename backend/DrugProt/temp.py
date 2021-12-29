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
