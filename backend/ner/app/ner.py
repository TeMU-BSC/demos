
from os import environ, path, walk
from statistics import mean
from time import time
from typing import Dict, List
from flask import g, json, request, jsonify
from flask_cors import CORS
from app import app
import numpy as np
import os
import shutil
from preprocess import preprocess_darryl_V1
from rapidfuzz import fuzz,process
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from load_models import get_predict
from norm_to_darryl.baseline.baseline_norm import  get_normalized

import pickle




from NER_utils.conll_to_brat import conll_to_brat, output_brat
# model_dir = 'procedimiento/model-complete'
# data_pickle_path = ''
# json_path = 'data'
# dicts_dir = ''
# config_path = 'config.txt'


print("API READY")
CORS(app)

models = ['procedimiento','enfermedad','farmaco','sintoma']
with open('decs2020.json', 'r') as file:
     terms = json.load(file)


def save_obj(directory, obj, name):
   '''Helper function using pickle to save and load objects'''
   with open(os.path.join(directory, name + '.pkl'), 'wb+') as f:
       pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


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
                  brat_original_folder_test, brat_output_folder_test, overwrite=True)


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
                
        
        temp_file_reader_1 = temp_file_reader.split('\n')
        temp_file_reader_1 = [i for i in temp_file_reader_1 if i != '']
        output = []
        for i in temp_file_reader_1:
            dic = {}
            datos = i.split('\t')
            dic['A-ID']  = datos[0] 
            dic['B-TYPE'] = datos[1]
            dic['C-START'] = datos[2]
            dic['D-END'] = datos[3]
            dic['E-text'] = datos[4]
            dic['F-snomed'] = datos[5]
            output.append(dic)
        file_dict[head[0]] = output

        # file_temp = 'brat-pred'+models[0]
        # with open(os.path.join(file_temp, f)) as file_object:
        #     head = f.split('.')
        #     file_dict[head[0]] = file_object.read()

    # try:
    #     shutil.rmtree('brat')
    #     shutil.rmtree('brat-bio')
    #     for model in models: 
    #         dir_to_delete = 'brat-pred'+model
    #         shutil.rmtree(dir_to_delete)
    # except OSError as e:
    #     print("Error: %s - %s." % (e.filename, e.strerror))

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


@app.route('/hello', methods=['GET'])
def hello():
    return "HELLO FROM NER<"


@app.route('/get_annotations', methods=['POST'])
def get_annotations():
    json_input = request.json
    if json_input['ner_type'] != 'All':
        global models
        models = [json_input['ner_type']]
    else:
        models = ['enfermedad', 'farmaco', 'sintoma', 'procedimiento']
    json_to_file = {
        'INPUTTEXT': json_input['INPUTTEXT'].rstrip()
    }
    with open("input_data.json","w") as f:
        json.dump(json_to_file,f)

    # clean_server()
    for model in models:
        print(model)
        json_path = 'input_data.json'
        dicts_dir = model+'/'
        config_path = model+'/config.txt'
        # Load data
        parsed_json, aux = preprocess_darryl_V1(json_path, config_path, dicts_dir)
        answ = get_predict(model,x=[parsed_json['token_idx'], parsed_json['char_idx'], parsed_json['bpe']])
        predict_label = np.argmax(answ, axis=2)
        conll_predictions_outpath = os.path.join(dicts_dir, 'test_predictions_v1.bio')
        reconstruct_conll(dicts_dir, aux, predict_label, conll_predictions_outpath)
        reconstruct_brat(json_path,'brat-pred'+model , conll_predictions_outpath)
        get_normalized('brat-pred'+model+"/",'brat-pred'+model+"/")
    
    return jsonify(getAnnotationResult())

@app.route('/get_mesh', methods=['POST'])
def get_mesh():
    mesh = []
    annotations = request.json
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

