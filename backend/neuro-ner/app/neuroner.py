from crypt import methods
from flask import g, json, request, jsonify
from flask_cors import CORS
from app import app
import numpy as np
import os
import shutil
import subprocess
from subprocess import Popen, PIPE, check_output

CORS(app)

@app.route('/', methods=['GET'])
def hello1():
    return "HELLO FROM Neuro NER"

@app.route('/hello', methods=['GET'])
def hello():
    return "HELLO FROM Neuro NER"


# def getAnnotationResults():
#     ext = ".ann"
#     file_dict =  {}
#     ann_files = [i for i in os.listdir("sample_data/out/brat/deploy") if os.path.splitext(i)[1] == ext]
#     for f in ann_files:
#         temp_file_reader = ""
#         with open(os.path.join("sample_data/out/brat/deploy", f)) as file_object:
#             head = f.split('.')
#             temp_file_reader = temp_file_reader + file_object.read()

#     temp_file_reader_1 = temp_file_reader.split('\n')
#     temp_file_reader_1 = [i for i in temp_file_reader_1 if i != '']
#     output = []
#     for i in temp_file_reader_1:
#         dic = {}
#         datos = i.split('\t')
#         print(datos)
#         dic['A-ID']  = datos[0] 
#         datos2 = datos[1].split(" ")
#         dic['B-TYPE'] = datos2[0]
#         dic['C-START'] = datos2[1]
#         dic['D-END'] = datos2[2]
#         dic['E-TEXT'] = datos[2]
#         output.append(dic)
    
#     file_dict[head[0]] = output

#     try:
#         shutil.rmtree('sample_data/out')
#         os.remove('sample_data/deploy/texto.txt')
#         os.remove('sample_data/deploy_spacy_bioes.out')
#         os.remove('sample_data/deploy_spacy_bioes.txt')
#         os.remove('sample_data/deploy_spacy.txt')
#         print("Borrar")
#     except OSError as e:
#         print("Error: %s - %s." % (e.filename, e.strerror))
#     return file_dict
    
# @app.route('/get_annotations', methods=['POST'])
# def get_annotations():
#     json_input = request.json

#     ##Save input data as file, since initial code was done for files
#     with open("sample_data/deploy/texto.txt", "w") as input:
#         input.write(json_input['INPUTTEXT'].rstrip())
#     #Run script which sends data to model.
#     command = "python -W ignore main.py --config demo.decode.config"
#     try:
#         output = subprocess.check_output(command, shell=True)
#     except subprocess.CalledProcessError as e:
#         print(e.output)
#         return jsonify({'error': e.output})

#     # Read output data.


    

#     return jsonify(getAnnotationResults())