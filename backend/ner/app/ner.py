
from os import environ, path, walk
from statistics import mean
from time import time
from typing import Dict, List
from flask import g, json, request, jsonify
from flask_cors import CORS
from app import app
import numpy as np
import tensorflow as tf
import pickle
import os

from preprocess import preprocess_darryl_V1

from NER_utils.conll_to_brat import conll_to_brat
model_dir = 'model-complete'
data_pickle_path = ''
json_path = 'data'
dicts_dir = ''
config_path = 'config.txt'
# Load model
new_model = tf.keras.models.load_model(model_dir)
print("API READY")
CORS(app)


def reconstruct_conll(dicts_dir, aux, test_predict_label, outpath):
    """
    Parameters
    ----------
    dicts_dir : string
        DESCRIPTION.
    aux : dictionary
        Last output from preprocessing function.
    test_predict_label : numpy
        Output from np.argmax(test_predict,axis=2)
    outpath : string
        Path to output file 
    Returns
    -------
    None.
    """
    # Load tag2idx dictionary and invert it
    with open(os.path.join(dicts_dir, 'tag2idx.json'), 'r') as f:
        tag2idx = json.load(f)
    idx2tag = {v: k for k, v in tag2idx.items()}

    # Reconstruct CONLL
    with open(outpath, 'w') as fout:
        for sentence, files, positions0, positions1, labels in zip(aux['tokens'], aux['files'], aux['pos0'], aux['pos1'], test_predict_label):
            for token, _file_, pos0, pos1, label in zip(sentence, files, positions0, positions1, labels):
                tag = idx2tag[label]
                fout.write('{} {} {} {} {}\n'.format(
                    token, _file_, pos0, pos1, tag))

    fout.close()


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
                  brat_original_folder_test, brat_output_folder_test, overwrite=False)


def getAnnotationResult():
    ext = '.ann'
    file_dict = {}
    ann_files = [i for i in os.listdir(
        'brat-pred') if os.path.splitext(i)[1] == ext]
    # Iterate over your txt files
    for f in ann_files:
        # Open them and assign them to file_dict
        with open(os.path.join('brat-pred', f)) as file_object:
            head = f.split('.')
            file_dict[head[0]] = file_object.read()

    # try:
    #     shutil.rmtree('brat')
    #     shutil.rmtree('brat-bio')
    #     shutil.rmtree('brat-pred')
    # except OSError as e:
    #     print("Error: %s - %s." % (e.filename, e.strerror))

    return file_dict


# def clean_server():

#     try:
#         shutil.rmtree('brat')
#         shutil.rmtree('brat-bio')
#         shutil.rmtree('brat-pred')
#     except OSError as e:
#         print("Error: %s - %s." % (e.filename, e.strerror))


@app.route('/hello', methods=['POST'])
def hello():
    return jsonify(request.json.get("INPUTTEXT")+"Respuesta")


@app.route('/get_annotations', methods=['POST'])
def get_annotations():
    json_input = request.json

    # clean_server()
    json_path = 'data'
    dicts_dir = ''
    config_path = 'config.txt'
    parsed_json, aux = preprocess_darryl_V1(
        json_input, json_path, config_path, dicts_dir)
    print(json_input)
    token_idx = np.asarray(parsed_json['token_idx'], dtype=np.float32)
    char_idx = np.asarray(parsed_json['char_idx'], dtype=np.float32)
    bpe = np.asarray(parsed_json['bpe'], dtype=np.float32)
    answ = new_model.\
        predict(x=[token_idx, char_idx, bpe])
    predict_label = np.argmax(answ, axis=2)
    conll_predictions_outpath = os.path.join(
        dicts_dir, 'test_predictions_v1.bio')
    reconstruct_conll(dicts_dir, aux, predict_label, conll_predictions_outpath)
    # Darryl: Output folder where you want to store your Brat files. Put the route you want here
    outpath = os.path.join(dicts_dir, 'brat-pred')
    reconstruct_brat(json_path, outpath, conll_predictions_outpath)
    return jsonify(getAnnotationResult())
