
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
import shutil
from preprocess import preprocess_darryl_V1
from rapidfuzz import fuzz,process
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


from NER_utils.conll_to_brat import conll_to_brat
model_dir = 'procedimiento/model-complete'
data_pickle_path = ''
json_path = 'data'
dicts_dir = ''
config_path = 'config.txt'
# Load model
procedimiento_model = tf.keras.models.load_model(model_dir)
enfermedad_model = tf.keras.models.load_model('enfermedad/model-complete')
farmaco_model = tf.keras.models.load_model('enfermedad/model-complete')
sintoma_model = tf.keras.models.load_model('sintoma/model-complete')
print("API READY")
CORS(app)

models = ['procedimiento','enfermedad','farmaco','sintoma']
models_keras = {
    'procedimiento':procedimiento_model,
    'enfermedada':enfermedad_model,
    'farmaco': farmaco_model,
    'sintoma': sintoma_model
}


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
        'brat-pred'+models[0]) if os.path.splitext(i)[1] == ext]
    # Iterate over your txt files
    for f in ann_files:
        temp_file_reader = ""
        # Open them and assign them to file_dict
        for model in models:
            file_temp = 'brat-pred'+model
            with open(os.path.join(file_temp, f))  as file_object:
                head = f.split('.')
                temp_file_reader =  temp_file_reader + file_object.read()
        
        file_dict[head[0]] = temp_file_reader

        # file_temp = 'brat-pred'+models[0]
        # with open(os.path.join(file_temp, f)) as file_object:
        #     head = f.split('.')
        #     file_dict[head[0]] = file_object.read()

    try:
        shutil.rmtree('brat')
        shutil.rmtree('brat-bio')
        for model in models: 
            dir_to_delete = 'brat-pred'+model
            shutil.rmtree(dir_to_delete)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    return file_dict


def clean_server():

    try:
        shutil.rmtree('brat')
        shutil.rmtree('brat-bio')
        shutil.rmtree('brat-predenfermedad')
        shutil.rmtree('brat-predfarmaco')
        shutil.rmtree('brat-predsintoma')
        shutil.rmtree('brat-predprocedimiento')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


@app.route('/hello', methods=['POST'])
def hello():
    return jsonify(request.json.get("INPUTTEXT")+"Respuesta")


@app.route('/get_annotations', methods=['POST'])
def get_annotations():
    json_input = request.json

    clean_server()
    for model in models:
        json_path = 'data'+model
        dicts_dir = model+'/'
        config_path = model+'/config.txt'
        parsed_json, aux = preprocess_darryl_V1(json_input, json_path, config_path, dicts_dir)
        token_idx = np.asarray(parsed_json['token_idx'], dtype=np.float32)
        char_idx = np.asarray(parsed_json['char_idx'], dtype=np.float32)
        bpe = np.asarray(parsed_json['bpe'], dtype=np.float32)
        answ = procedimiento_model.\
            predict(x=[token_idx, char_idx, bpe])
        predict_label = np.argmax(answ, axis=2)
        conll_predictions_outpath = os.path.join(dicts_dir, 'test_predictions_v1.bio')
        reconstruct_conll(dicts_dir, aux, predict_label, conll_predictions_outpath)
        reconstruct_brat(json_path,'brat-pred'+model , conll_predictions_outpath)
    # json_path = 'data'
    # json_path_enfermedad = 'data_enfermedad'
    # dicts_dir = 'procedimiento/'
    # dicts_dir_enfermedad = 'enfermedad/'
    # config_path = 'procedimiento/config.txt'
    # config_path_enfermedad = 'enfermedad/config.txt'
    # parsed_json, aux = preprocess_darryl_V1(
    #     json_input, json_path, config_path, dicts_dir)
    # parsed_json_enfermedad, aux_enfermedad = preprocess_darryl_V1(json_input, json_path_enfermedad,config_path_enfermedad,dicts_dir_enfermedad)
    # token_idx_enfermedad = np.array(parsed_json_enfermedad['token_idx'], dtype=np.float32)
    # char_idx_enfermedad = np.asarray(parsed_json['char_idx'], dtype=np.float32)
    # bpe_enfermedad = np.asarray(parsed_json['bpe'], dtype=np.float32)
    # print(json_input)
    # token_idx = np.asarray(parsed_json['token_idx'], dtype=np.float32)
    # char_idx = np.asarray(parsed_json['char_idx'], dtype=np.float32)
    # bpe = np.asarray(parsed_json['bpe'], dtype=np.float32)
    # answ = procedimiento_model.\
    #     predict(x=[token_idx, char_idx, bpe])
    # answ_enfermedad = enfermedad_model.\
    #     predict(x=[token_idx_enfermedad,char_idx_enfermedad, bpe_enfermedad])
    # predict_label = np.argmax(answ, axis=2)
    # predict_label_enfermedad = np.argmax(answ_enfermedad, axis=2)
    # conll_predictions_outpath = os.path.join(
    #     dicts_dir, 'test_predictions_v1.bio')
    # conll_predictions_outpath_enfermedad = os.path.join(dicts_dir_enfermedad, 'test_predictions_v1.bio')
    # reconstruct_conll(dicts_dir, aux, predict_label, conll_predictions_outpath)
    # reconstruct_conll(dicts_dir_enfermedad,aux_enfermedad,predict_label_enfermedad, conll_predictions_outpath_enfermedad)
    # #Darryl: Output folder where you want to store your Brat files. Put the route you want here
    # outpath = os.path.join(dicts_dir, 'brat-pred')
    # outpath_enfermedad = os.path.join(dicts_dir, 'brat-pred-enfermedad')
    # reconstruct_brat(json_path, 'brat-pred', conll_predictions_outpath)
    # reconstruct_brat(json_path_enfermedad, 'brat-pred-enfermedad', conll_predictions_outpath_enfermedad)
    return jsonify(getAnnotationResult())

@app.route('/get_mesh', methods=['POST'])
def get_mesh():
    mesh = []
    annotations = request.json
    with open('decs2020.json', 'r') as file:
     terms = json.load(file)
    for annotation in annotations:
        found_result = []
        text_tokens = word_tokenize(annotation)
        text_without_sw = [word for word in text_tokens if not word in stopwords.words('spanish')]
        annotation = " ".join(text_without_sw)
        for term in terms: 
            for syno in term["synonyms"]:
                if(fuzz.token_set_ratio(annotation,syno) > 90):
                    found_result.append ({"annotation": annotation,"name":syno, "code": term["code"],"description": term["description"], "score":fuzz.token_set_ratio(annotation,syno)})
                    break
        found_result.sort(key=lambda x: x["score"], reverse=True)
        if(len(found_result) >= 1):
            mesh.append(found_result[0])
    return jsonify(mesh)

