#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 15:45:11 2021

@author: antonio
"""
from NER_utils.embeddings import getEmbeddingMatrix
from NER_utils.conll_to_brat import conll_to_brat
from NER_utils.ner_evaluation import metrics_main
from NER_utils.copy_files import copy_files

from preprocess import preprocess
from network import create_ner_model
from common import parse_config_file, save_obj, load_obj, write_config

from tensorflow.keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint
from tensorflow.keras.metrics import Recall, Precision
from tensorflow.keras.optimizers import Nadam
from tensorflow.keras.models import model_from_json


import fasttext
from pathlib import Path
import os
import sys
import time
# from tensorflow.keras.models import load_weights

import argparse

def argparser():
    
    parser = argparse.ArgumentParser(description='process user given parameters')
    parser.add_argument("--brat_path", required = True, dest = "brat_path", 
                        help = "absolute path to folder with Brat files")
    parser.add_argument("--bio_path", required=False, default=None,dest = 'bio_path',
                        help = "absolute path to folder with BIO files")
    parser.add_argument("--embedding_path", required = True, dest = "embedding_path", 
                        help = "absolute path to binary FastText word embedding file")
    parser.add_argument("--file_lists", required = False, default=None, dest = "file_lists_path", 
                        help = "path to directory where I have file lists to evaluate separately")
    parser.add_argument("--pretrained_weights", required = False, default=None, 
                        dest = "pretrained_weights_path",
                        help = "path to hdf5 file with pretrained weights")
    parser.add_argument("--out_path", required = True, dest = "out_path", 
                        help = "absolute path to output folder")
    parser.add_argument("--LSTM_hiddenDim", required = False, default=100,
                        dest = "LSTM_hiddenDim", 
                        help = "hidden units in main LSTM")
    parser.add_argument("--dropout_bilstm", required = False, default=0.5,
                        dest = "dropout_bilstm", 
                        help = "dropout in main LSTM")
    parser.add_argument("--char_embedd_length", required = False, default=25,
                        dest = "char_embedd_length", 
                        help = "Character embedding size")
    parser.add_argument("--char_LSTM_units", required = False, default=25,
                        dest = "char_LSTM_units", 
                        help = "hidden units in character embedding LSTM")

    args =  parser.parse_args() 
    
    return (args.brat_path, args.bio_path, args.embedding_path, args.pretrained_weights_path, 
            args.file_lists_path, args.out_path, int(args.LSTM_hiddenDim), 
            float(args.dropout_bilstm), int(args.char_embedd_length), int(args.char_LSTM_units))
    

def main(brat_path, bio_path, embedding_path, pretrained_weights_path, file_lists_path, out_path, 
 LSTM_hiddenDim, dropout_bilstm, char_embedd_length, char_LSTM_units):
    
    out_path = (out_path + f"-LSTM_hiddenDim-{LSTM_hiddenDim}-" +
            f"dropout_bilstm-{dropout_bilstm}-" +
            f"char_embedd_length-{char_embedd_length}-" +
            f"char_LSTM_units-{char_LSTM_units}-darryl")
        
    # Create output directories
    Path(out_path).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(out_path, 'predictions', 'brat-test')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(out_path, 'predictions', 'brat-test-ehr')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(out_path, 'predictions', 'brat-test-covid')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(out_path, 'predictions', 'brat-test-eme')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(out_path, 'predictions', 'brat-test-spaccc')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(out_path, 'tensorboard_logs')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(out_path, 'models')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(out_path, 'report')).mkdir(parents=True, exist_ok=True)
    
    # Redirect standard output and standard error
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    timestamp = int(time.time())
    f_stdout = open(os.path.join(out_path, f'{timestamp}.out'), 'w')
    f_stderr = open(os.path.join(out_path, f'{timestamp}.err'), 'w')
    sys.stdout = f_stdout
    sys.stderr = f_stderr

    if pretrained_weights_path == None:
        training = True
        print("Mode: Training + inference")
    else:
        training = False
        print("Mode: Loading model + Inference")
    

    ### Preprocess data
    t0_prepro = time.time()
    train_pad, dev_pad, test_pad, test, NUMCHARS, MAXLENGTH, MAXLENCHAR, \
        BPEDIM, token2idx, tag2idx = \
            preprocess(brat_path, bio_path, out_path,
                       pretrained_weights_path, training=training)
    print(f"Elapsed preprocessing time: {time.time() - t0_prepro}s")
    
    # # Temporarily save input data after prepro to save time when testing
    # save_obj(out_path, train_pad,"train_pad")
    # save_obj(out_path, dev_pad,"dev_pad")
    # save_obj(out_path, test_pad,"test_pad")

    
    # # DarryL: Load ALL input data without preprocessing to save time when testing
    # train_pad = load_obj(out_path, "train_pad")
    # dev_pad = load_obj(out_path, "dev_pad")
    # test_pad = load_obj(out_path, "test_pad")
    # token2idx = load_obj()
    # tag2idx = load_obj()
    # MAXLENGTH = 292
    # MAXLENCHAR = 10
    # BPEDIM = 50
    
    ### Load embedding matrix
    t0_emb = time.time()
    # Load FastText model
    ft = fasttext.load_model(embedding_path)
    # Generate embeddings matrix
    embedding_matrix = getEmbeddingMatrix(token2idx, ft.get_dimension(), ft)
    print(f"Elapsed loading FastText embedding matrix time: {time.time() - t0_emb}s")
    
    
    embedding_weights = embedding_matrix
    (vocab_size, embedding_size) = embedding_matrix.shape
    tag_size = len(tag2idx.keys())
    if training==False:
        # Load parameters from config.txt
        config = parse_config_file(os.path.join(os.path.dirname(pretrained_weights_path), "config.txt"))
        MAXLENGTH = int(config['maxSeqLength'])
        MAXLENCHAR = int(config['maxCharLength'])
        NUMCHARS = int(config['nChars'])
        BPEDIM = int(config['bpeDim'])
        LSTM_hiddenDim = int(config['hiddenDim'])
        dropout_bilstm = float(config['dropout_bilstm'])
        char_embedd_length = int(config['char_embedd_length'])
        char_LSTM_units = int(config['char_LSTM_units'])
        use_crf = bool(config['use_crf'])
        use_bpe = bool(config['use_bpe'])
        
        # embedding_size_config = 
        # vocab_size_config = 
        # tag_size_config = 
        # assert embedding_size == embedding_size_config
        # assert vocab_size == vocab_size_config
        # assert tag_size == tag_size_config

        
        
    ### Initialize network
    model = \
        create_ner_model(maxSeqLength=MAXLENGTH, maxCharLength=MAXLENCHAR, nChars=NUMCHARS,
                         embeddingDim=embedding_size, vocabSize=vocab_size,
                bpeDim=BPEDIM, hiddenDim=LSTM_hiddenDim, dropout_bilstm=dropout_bilstm,
                char_embedd_length=char_embedd_length, char_LSTM_units=char_LSTM_units,
                tensorboard_path=os.path.join(out_path, "tensorboard_logs"),
                model_checkpoint_path=os.path.join(out_path, "models"), 
                weight=[embedding_weights,], target=tag_size, 
                path=os.path.join(out_path, "models/model_neuroNER.h5"), 
                validation_split=0.15, mask=False, use_crf=True, use_bpe=True)
    print("Network correctly created")
    if training==True:
        
        write_config(MAXLENGTH, MAXLENCHAR, NUMCHARS, embedding_size, vocab_size,
             BPEDIM, LSTM_hiddenDim, dropout_bilstm, char_embedd_length,
             char_LSTM_units, os.path.join(out_path, "tensorboard_logs"), 
             os.path.join(out_path, "models"),
             tag_size, use_crf=True, use_bpe=True)
            
        metrics = [Recall(), Precision()]   
        opt = Nadam(learning_rate=0.001)
        use_crf=False
        if use_crf==True:
          # model.compile(loss=crf.loss, optimizer=opt,
          #         metrics = metrics)
          model.compile(optimizer=opt, metrics = metrics)  # https://github.com/xuxingya/tf2crf
        else:
          model.compile(optimizer=opt, loss='categorical_crossentropy',
                  metrics = metrics)  
    
    
        ### Train
        chp_path = os.path.join(os.path.join(out_path, "models"), 'model-{epoch:02d}.hdf5')
        callbacks = [EarlyStopping(monitor="val_loss",patience=3),
                    #TensorBoard(log_dir=self.tb_path), # If https://github.com/xuxingya/tf2crf
                    ModelCheckpoint(filepath=chp_path,
                                    save_weights_only=True, monitor='val_loss',
                                    mode='max', save_best_only=False)] 
        print("\nTrain...")
        t0_train = time.time()
        epoch = 3
        model.fit(x=[[train_pad['token_idx']], [train_pad['char_idx']], [train_pad['bpe']]],
                  y=train_pad['tag_idx_1hot'], # train_y must have dimensions (N_sentences, MAXLENGTH, tag_size) (in my first iteration, it is (N_sentences, 91, 9)),
                  batch_size=16,
                  epochs=epoch,
                  validation_data=([[dev_pad['token_idx']], [dev_pad['char_idx']], [dev_pad['bpe']]],
                                   dev_pad['tag_idx_1hot']),
                  callbacks = callbacks)
    
        print(f"Elapsed training time: {time.time() - t0_train}s")
        # json_config = model.to_json()
        # with open(os.path.join(out_path, 'models','model-architecture.json'), 'w') as json_file:
        #     json_file.write(json_config)
        model.save(os.path.join(out_path, 'models','model-complete'))
        model.save_weights(os.path.join(out_path, 'models','model-final-weights.h5'))
        #model.base_model.save_weights(os.path.join(out_path, 'models','base-model-final-weights.h5'))
        print(f"Saved final model in {os.path.join(out_path, 'models', 'model-final-weights.h5')}")

    else:
        model.build([(None,MAXLENGTH),(None,MAXLENGTH,MAXLENCHAR),(None,MAXLENGTH,BPEDIM)])
        # model = model_from_json(os.path.join(os.path.dirname(pretrained_weights_path), "model-architecture.json"))
        model.load_weights(pretrained_weights_path)
        print(f"Weights loaded from {pretrained_weights_path}")
        
    ### Predict
    print("\nPredict...")
    t0_infer = time.time()
    test_predict = model.\
        predict(x=[test_pad['token_idx'], test_pad['char_idx'], test_pad['bpe']])
    # test_predict_label = np.argmax(test_predict,axis=2) # remove if CRF https://github.com/xuxingya/tf2crf
    print(f"Elapsed inference time: {time.time() - t0_infer}s")
    
    
    ### Reconstruct CONLL
    t0_reconstruct = time.time()
    conll_predictions_outpath = os.path.join(out_path, 'predictions/test_predictions_v1.bio')
    idx2tag = {v: k for k, v in tag2idx.items()}
    with open(conll_predictions_outpath, 'w') as fout:
      # for sentence, files, positions0, positions1, labels in zip(test['tokens'], test['files'], test['pos0'], test['pos1'], test_predict_label):
      for sentence, files, positions0, positions1, labels in zip(test['tokens'], test['files'], test['pos0'], test['pos1'], test_predict): # if CRF https://github.com/xuxingya/tf2crf
        for token, _file_, pos0, pos1, label in zip(sentence, files, positions0, positions1, labels):
          tag = idx2tag[label]
          fout.write('{} {} {} {} {}\n'.format(token, _file_, pos0, pos1, tag))
    print(f"Elapsed CONLL reconstruction time: {time.time() - t0_reconstruct}s")
      

    ### CONLL2Brat
    t0_conll2brat = time.time()
    brat_original_folder_test = os.path.join(brat_path, 'test')
    brat_output_folder_test = os.path.join(out_path, 'predictions/brat-test')
    conll_input_filepath_test = conll_predictions_outpath
    conll_output_filepath_test = conll_input_filepath_test
    
    conll_to_brat(conll_input_filepath_test, conll_output_filepath_test, 
                  brat_original_folder_test, brat_output_folder_test, overwrite=False)
    print(f"Elapsed CONLL2Brat time: {time.time() - t0_conll2brat}s")
    
    
    ### Evaluate ALL predictions
    t0_eval = time.time()
    gs_test = brat_original_folder_test
    predictions_test = brat_output_folder_test
    metrics_main(gs_test, predictions_test, ['PROCEDIMIENTO'], subtask='ner')
    print(f"Elapsed evaluation time: {time.time() - t0_eval}s")
    
    if file_lists_path != None:
        file_lists = os.listdir(file_lists_path)
        
        for l in file_lists:
            print("----------------------------------------------------------------")
            
            if l == 'spaccc.txt':
                ### Evaluate only SPACCC predictions
                print("\n\nEvaluate only SPACCC predictions")
                brat_output_folder_test_subset = os.path.join(out_path, 'predictions/brat-test-spaccc')
                
            elif l == 'covid.txt':
                ### Evaluate only COVID predictions
                print("\n\nEvaluate only COVIDCCC predictions")
                brat_output_folder_test_subset = os.path.join(out_path, 'predictions/brat-test-covid')
                
            elif l == 'eme.txt':
                ### Evaluate only emeccc predictions
                print("\n\nEvaluate only emeccc predictions")
                brat_output_folder_test_subset = os.path.join(out_path, 'predictions/brat-test-eme')
                
            elif l == 'ehr.txt':
                ### Evaluate only EHR predictions
                print("\n\nEvaluate only EHR predictions")
                brat_output_folder_test_subset = os.path.join(out_path, 'predictions/brat-test-ehr')
            else: 
                print(l)
                continue
            print(l)
            file_list = [line.strip() for line in open(os.path.join(file_lists_path, l), 'r')]
            copy_files(predictions_test, brat_output_folder_test_subset, file_list)
            metrics_main(gs_test, predictions_test, ['PROCEDIMIENTO'], subtask='ner', filelist=file_list)
    
    # TODO: add scipacy and spacy tokenization
    # TODO: add post-processing rules
    # TODO: add POS (and gazetteer) embeddings (flags)
    # TODO: add data augmentation
    # TODO: proper logging
    # TODO: create parameters filepath to specify all parameters
    # TODO: add parametrization for preprocessing, postprocessing and network
    
    f_stdout.close()
    f_stderr.close()
    sys.stdout = original_stdout
    sys.stderr = original_stderr

if __name__ == '__main__':
       
    (brat_path, bio_path, embedding_path, pretrained_weights_path, file_lists_path, out_path, 
     LSTM_hiddenDim, dropout_bilstm, char_embedd_length, char_LSTM_units) = argparser()
    
    main(brat_path, bio_path, embedding_path, pretrained_weights_path, file_lists_path, out_path, 
     LSTM_hiddenDim, dropout_bilstm, char_embedd_length, char_LSTM_units)
    

