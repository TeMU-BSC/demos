#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 11:16:01 2021

@author: antonio
"""
import pickle
import os
def load_obj(directory, name):
    '''Helper function using pickle to save and load objects'''
    with open(os.path.join(directory,name + ".pkl"), "rb") as f:
        return pickle.load(f)

def save_obj(directory, obj, name):
    '''Helper function using pickle to save and load objects'''
    with open(os.path.join(directory, name + '.pkl'), 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
def parse_config_file(config_file_path):
    config_params = {}
    with open(config_file_path) as f:
        for line in f:
            config_params[line.split('=')[0]] = line.split('=')[-1].strip()
    return config_params
            


def write_config(maxSeqLength, maxCharLength, nChars, embeddingDim, vocabSize,
                 bpeDim, hiddenDim, dropout_bilstm, char_embedd_length,
                 char_LSTM_units, tensorboard_path, model_checkpoint_path,
                 target, use_crf, use_bpe):
    print(f"maxSeqLength={maxSeqLength}\n"+
          f"maxCharLength={maxCharLength}\n"+
f"nChars={nChars}\n"+
f"embeddingDim={embeddingDim}\n"+
f"bpeDim={bpeDim}\n"+
f"tensorboard_path={tensorboard_path}\n"+
f"model_checkpoint_path={model_checkpoint_path}\n"+
f"vocabSize={vocabSize}\n"+
f"target={target}\n"+
f"hiddenDim={hiddenDim}\n"+
f"dropout_bilstm={dropout_bilstm}\n"+
f"char_embedd_length={char_embedd_length}\n"+
f"char_LSTM_units={char_LSTM_units}\n"+
f"use_crf={use_crf}\n"+
f"use_bpe={use_bpe}\n"+
f"embeddingDim={embeddingDim}\n", file=open(os.path.join(model_checkpoint_path, "config.txt"), 'w'))