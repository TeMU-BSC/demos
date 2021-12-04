#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 15:27:33 2021

@author: antonio
"""
"""
from NER_utils.brat_to_conll import brat_to_conll
from NER_utils.split_bio import split_bio
import numpy as np
from NER_utils.embeddings import add_bpe_emb
from NER_utils.transform2idx import word2int, get_char_idx, label2vec
from tensorflow.keras.preprocessing.sequence import pad_sequences
from bpemb import BPEmb
import os
from pathlib import Path
from common import load_obj, save_obj, parse_config_file


def Flatten(ul):
    fl = []
    for i in ul:
        if type(i) is list:
            fl += Flatten(i)
        else:
            fl += [i]
    return fl

def pad_dataset(dataset, MAXLENGTH):
  padded_dataset = {}
  padded_dataset['token_idx'] = pad_sequences(dataset['token_idx'],maxlen=MAXLENGTH,padding="post")
  padded_dataset['tag_idx'] = pad_sequences(dataset['tags_idx'],maxlen=MAXLENGTH,padding="post")
  padded_dataset['files'] = list(map(lambda x: x[0], dataset['files']))
  return padded_dataset
  
def preprocess(brat_path, bio_path, out_path, pretrained_model_path=None, training=True):

    if training!=True:
        # Parse config parameters
        config = parse_config_file(os.path.join(os.path.dirname(pretrained_model_path), "config.txt"))
        
    ### Brat2BIO ###
    if bio_path == None:
        bio_path = brat_path + "-bio"
        Path(brat_path + "-bio").mkdir(parents=True, exist_ok=True)
        if training==True:
            partitions = ['train', 'dev', 'test']
        else:
            partitions = ['test']
        for partition in partitions:
            brat_to_conll(os.path.join(brat_path, partition), 
                          os.path.join(bio_path, partition + '.bio'), 'en')


    ### Parse BIO ###
    if training==True:
        train = split_bio(os.path.join(bio_path, 'train.bio'))
        dev = split_bio(os.path.join(bio_path, 'dev.bio'))
    test = split_bio(os.path.join(bio_path, 'test.bio'))
    
    # TODO: check there are no empty tokens in BIO file: that breaks the BPE Embedding


    ### Token2idx
    # Get words in dataset and token2idx dictionary
    if training==True:
        tokens = set(Flatten(train['tokens'])).union(set(Flatten(dev['tokens']))).union(set(Flatten(test['tokens'])))
        token2idx = {w: i + 2 for i, w in enumerate(tokens)}
        token2idx["#ENDPAD"] = 0
        token2idx["UNK"] = 1
        save_obj(os.path.join(out_path, "models"), token2idx, "token2idx")
    else:
        # Load token2idx from file
        token2idx = load_obj(os.path.join(out_path, "models"), "token2idx")


    # Map tokens to idx
    if training==True:
        train['token_idx'] = word2int(train['tokens'], token2idx)
        dev['token_idx'] = word2int(dev['tokens'], token2idx)
    test['token_idx'] = word2int(test['tokens'], token2idx)
    

    ### Tag2idx
    if training==True:
        tags = set(Flatten(train['tags'])).union(set(Flatten(dev['tags']))).union(set(Flatten(test['tags'])))
        tag2idx = {w: i for i, w in enumerate(sorted(tags, reverse=True))}
        train['tags_idx'] = word2int(train['tags'], tag2idx)
        dev['tags_idx'] = word2int(dev['tags'], tag2idx)
        test['tags_idx'] = word2int(test['tags'], tag2idx)
        save_obj(os.path.join(out_path, "models"), tag2idx, "tag2idx")
    else:
        # Load tag2idx from file
        tag2idx = load_obj(os.path.join(out_path, "models"), "tag2idx")
        test['tags_idx'] = word2int(test['tags'], tag2idx)
    
    
    ### Padding
    if training==True:
        MAXLENGTH = max(map(lambda x: len(x), train['tokens']))
        train_pad = pad_dataset(train, MAXLENGTH)
        dev_pad = pad_dataset(dev, MAXLENGTH)
        test_pad = pad_dataset(test, MAXLENGTH)
    else:
        # Load MAXLENGTH from config file
        MAXLENGTH = int(config['maxSeqLength'])
        test_pad = pad_dataset(test, MAXLENGTH)

    ### Char2idx
    if training==True:
        # Build char2idx dict
        chars = set([char for sentence in train['tokens'] for token in sentence for char in token])
        NUMCHARS = len(chars)
        char2idx = {c: i + 2 for i, c in enumerate(chars)}
        char2idx["UNK"] = 1
        char2idx["PAD"] = 0
        MAXLENCHAR = 10
        
        train_pad['char_idx'] = np.asarray(get_char_idx(train, char2idx, MAXLENGTH, MAXLENCHAR), dtype=np.int64)
        dev_pad['char_idx'] = np.asarray(get_char_idx(dev, char2idx, MAXLENGTH, MAXLENCHAR), dtype=np.int64)
        test_pad['char_idx'] = np.asarray(get_char_idx(test, char2idx, MAXLENGTH, MAXLENCHAR), dtype=np.int64)
        
        save_obj(os.path.join(out_path, "models"), char2idx, "char2idx")
    else:
        # Load NUMCHARS and MAXLENCHAR from config file
        NUMCHARS = int(config['nChars'])
        MAXLENCHAR = int(config['maxCharLength'])
        # Load char2idx from file
        char2idx = load_obj(os.path.join(out_path, "models"), "char2idx")
        
        test_pad['char_idx'] = np.asarray(get_char_idx(test, char2idx, MAXLENGTH, MAXLENCHAR), dtype=np.int64)


    ### One-hot-encode labels
    tag_size = len(tag2idx.keys())
    if training==True:
        train_pad['tag_idx_1hot'] = label2vec(train_pad['tag_idx'], classes=tag_size)
        dev_pad['tag_idx_1hot'] = label2vec(dev_pad['tag_idx'], classes=tag_size)
    test_pad['tag_idx_1hot'] = label2vec(test_pad['tag_idx'], classes=tag_size)


    ### BPE Embedding
    if training==True:
        BPEDIM = 50
        bpemb_es = BPEmb(lang="es", dim=BPEDIM)
        
        train_pad['bpe'] = add_bpe_emb(train, bpemb_es, MAXLENGTH, BPEDIM)
        dev_pad['bpe'] = add_bpe_emb(dev, bpemb_es, MAXLENGTH, BPEDIM)
        test_pad['bpe'] = add_bpe_emb(test, bpemb_es, MAXLENGTH, BPEDIM)
    else:
        # Load BPEDIM from config file
        BPEDIM = int(config['bpeDim'])
        
        bpemb_es = BPEmb(lang="es", dim=BPEDIM)
        train_pad = None
        dev_pad = None
        test_pad['bpe'] = add_bpe_emb(test, bpemb_es, MAXLENGTH, BPEDIM)
    
    return train_pad, dev_pad, test_pad, test, NUMCHARS, MAXLENGTH, MAXLENCHAR, BPEDIM, token2idx, tag2idx
"""

############################################################################


# from tensorflow.keras.models import load_weights




import json, re
import os
import fasttext
from pathlib import Path
import sys
import time
import argparse
import numpy as np
from bpemb import BPEmb
from NER_utils.brat_to_conll import brat_to_conll
from NER_utils.embeddings import add_bpe_emb
from NER_utils.split_bio import split_bio
from NER_utils.transform2idx import word2int, get_char_idx, label2vec
from tensorflow.keras.preprocessing.sequence import pad_sequences
from common import load_obj, parse_config_file
def pad_dataset(dataset, MAXLENGTH):
    padded_dataset = {}
    padded_dataset['token_idx'] = pad_sequences(
        dataset['token_idx'], maxlen=MAXLENGTH, padding="post")
    padded_dataset['tag_idx'] = pad_sequences(
        dataset['tags_idx'], maxlen=MAXLENGTH, padding="post")
    padded_dataset['files'] = list(map(lambda x: x[0], dataset['files']))
    return padded_dataset


def json_to_txt(json_path, txt_path):
    """
    Transform JSON input into independent TXT files
    """
    with open(json_path, 'r') as f:
        files = json.load(f)
        
    Path(txt_path).mkdir(parents=True, exist_ok=True)
    for k,v in files.items():
        with open(os.path.join(txt_path, k + '.txt'), 'w') as fin:
           
            fin.write(re.sub(r"/\\n/g", '\n', v))


def preprocess_darryl_V1(json_path, config_path='', dicts_dir=''):
    """
    Take JSON with text files and output object ready to be input into 
    Keras model
    Parameters
    ----------
    json_path : str
        Path to JSON with text input.
    config_path : str, optional
        Path to model configuration file. The default is ''.
    dicts_dir : str, optional
        Path to directory with needed dictionaries. The default is ''.
    Returns
    -------
    test_pad : dict
        Python dict with numpy arrays as values.
    """

    config = parse_config_file(config_path)
        
    ### JSON to TXT ###
    txt_dir_path = os.path.join(os.path.dirname(json_path), 'brat')
    Path(txt_dir_path).mkdir(parents=True, exist_ok=True)
    json_to_txt(json_path, txt_dir_path)
    
    ### Brat2BIO ###
    # TODO: modify brat_to_conll to:
        # 1. Take JSON as input
        # 2. Do not create empty ANN
        # 3. Do not create temporary BIO file, but keep it as variable
    bio_path = txt_dir_path + "-bio"
    Path(bio_path).mkdir(parents=True, exist_ok=True)
    brat_to_conll(txt_dir_path, os.path.join(bio_path, 'test.bio'), 'es_core_news_sm')


    ### Parse BIO ###
    test = split_bio(os.path.join(bio_path, 'test.bio'))
    
    # TODO: check there are no empty tokens in BIO file: that break the BPE Embedding

    ### Token2idx ###
    # Load token2idx from file
    # token2idx = load_obj(dicts_dir, 'token2idx')
    with open(os.path.join(dicts_dir, 'token2idx.json'), 'r') as f:
        token2idx = json.load(f)


    # Map tokens to idx
    test['token_idx'] = word2int(test['tokens'], token2idx)
    

    ### Tag2idx
    # tag2idx = load_obj(dicts_dir, "tag2idx")
    with open(os.path.join(dicts_dir, 'tag2idx.json'), 'r') as f:
        tag2idx = json.load(f)
    test['tags_idx'] = word2int(test['tags'], tag2idx)
    
    
    ### Padding ###
    # Load MAXLENGTH from config file
    MAXLENGTH = int(config['maxSeqLength'])
    test_pad = pad_dataset(test, MAXLENGTH)

    ### Char2idx ###
    # Load NUMCHARS and MAXLENCHAR from config file
    MAXLENCHAR = int(config['maxCharLength'])
    # Load char2idx from file
    # char2idx = load_obj(dicts_dir, "char2idx")
    with open(os.path.join(dicts_dir, 'char2idx.json'), 'r') as f:
        char2idx = json.load(f)
    
    test_pad['char_idx'] = np.asarray(get_char_idx(test, char2idx, MAXLENGTH, MAXLENCHAR), dtype=np.int64)


    ### One-hot-encode labels ###
    tag_size = len(tag2idx.keys())
    test_pad['tag_idx_1hot'] = label2vec(test_pad['tag_idx'], classes=tag_size)


    ### BPE Embedding ###
    # Load BPEDIM from config file
    BPEDIM = int(config['bpeDim'])
    
    bpemb_es = BPEmb(lang="es", dim=BPEDIM)
    test_pad['bpe'] = add_bpe_emb(test, bpemb_es, MAXLENGTH, BPEDIM)
    
    return test_pad, test
