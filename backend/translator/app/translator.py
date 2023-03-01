'''
Main python script that runs the Flask app of the Translator Demo.

Author:
    Alejandro Asensio
    https://github.com/aasensios
'''

from os import environ, path, walk
import os
import subprocess
from subprocess import Popen, PIPE, check_output
from statistics import mean
from time import time
from typing import Dict, List
from io import StringIO
from flask import g, request, jsonify
from flask_cors import CORS 
from opennmt_caller import translate_sentence
from nltk import sent_tokenize
from app import app
import concurrent.futures


import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])   

import_or_install("ctranslate2")
import_or_install("sentencepiece")
import_or_install("nltk")
import_or_install("pandas")
import ctranslate2
import pandas as pd 
import nltk
import sentencepiece as spm
from nltk import sent_tokenize
nltk.download('punkt')
import os



CORS(app)

import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello from Translator Flask API!'


def convert_data_to_response(data: Dict) -> Dict:
    '''
    Wrap data within a standard API response skeleton with 'success', 'data'
    and 'message' keys.
    '''
    return {
        'success': True,
        'data': data,
        'message': 'Data retrieved successfully.'
    }


@app.route('/samples', methods=['GET'])
def get_samples():
    '''
    Get all text samples inside './samples/' directory.
    Returns a list of filenames and their respective content in a JSON format.
    '''
    samples = []
    for root, dirs, files in walk(environ.get('SAMPLES_DIR')):
        # print(root, dirs, files)
        for filename in files:
            # The two last letters describe the language
            lang_dir = root[-2:]
            # Read the content of each file
            with open(path.join(root, filename), 'r',encoding="utf-8") as current_file:
                content = current_file.read()
            # Append an object for each file
            samples.append({
                'language': lang_dir,
                'filename': filename,
                'content': content
            })
    return jsonify(convert_data_to_response(samples))


def get_translated_sentence(sentences, src,tgt) -> str:
    '''
    Get the translated sentence from the request.
    '''
    tic = time()
    text_ready = []
    spmodels = {"es":"sentencepieceModels/pten_esSP32k.model",
            "en":"sentencepieceModels/espt_enSP32k.model",
            "pt":"sentencepieceModels/enes_ptSP32k.model"
            }
    sp = spm.SentencePieceProcessor(model_file=spmodels[tgt])
    translator = ctranslate2.Translator(tgt, device="cpu",intra_threads=16)
    batch = sp.encode(sentences,out_type="str")
    for f in batch:
            f.insert(0,"__opt_tgt_"+tgt)
            f.insert(0,"__opt_src_"+src)
    result = translator.translate_batch(batch)
    for f in result:
        text_ready.append(sp.decode(f.hypotheses[0])+"\n")
    # if os.path.exists("/home/data/text.txt"):
    #     os.remove("/home/data/text.txt")
    # if os.path.exists("/home/data/log.txt"):
    #     os.remove("/home/data/log.txt")
    
    
    # for sentence in sentences:
    #     with open("/home/data/text.txt", "a", encoding="utf-8") as text_file:
    #             text_file.write(sentence + "\n")
                
    # command = "./tokenize_SP.sh -d /app/data -s {0} -t {1} -f /home/data/text.txt".format(src, tgt)
    # try:
    #     output = subprocess.check_output(command, shell=True)
    # except subprocess.CalledProcessError as e:
    #     print(e.output)
    #     return jsonify({'error': e.output})
    # toc = time()
    # print("Tokenizacion demoro = "+str(toc-tic))

    # command_1 = "./translate.sh -l {0}".format(tgt)
    # tic1 = time()
    # try:
    #     with Capturing() as output_1:
    #         run = subprocess.Popen(command_1, stdout=PIPE, shell=True)
    #         run.communicate()
        
    # except subprocess.CalledProcessError as e:
    #     print(e.output)
    #     return jsonify({'error': e.output})
    # toc1 = time()
    # print("Traducir demoro = "+str(toc1-tic1))
    # with open ("/home/data/text.translated.detokenized") as trans_text:
    #     text_ready = trans_text.readlines()
    
    return text_ready

    

@app.route('/translate', methods=['POST'])
def translate():
    '''
    Returns the corresponding translation regarding the source and target
    languages from the HTTP request body.

    The translation and translation time are obtained from other API called OpenNMT:
    http://forum.opennmt.net/t/simple-opennmt-py-rest-server/1392

    which is served in our virtual machine
    http://bsccnio01.bsc.es:5000/translator/translate

    The input HTTP request body must have the following format:
    {
        sourceLanguageCode: string (es|en|pt),
        targetLanguageCode: string (es|en|pt),
        text: string
    }

    The output HTTP response will have the following format:
    {
        success: boolean,
        data = {
            'sourceLanguage': string,
            'targetLanguage': string,
            'originalText': string,
            'translatedSentences': list of strings,
            'predictionScore': float,
            'translationTime': float
        },
        message: string
    }

    '''

    reponse = {
        "success": True,
        "data" : {
            'sourceLanguage': "",
            'targetLanguage': "",
            'originalText': "",
            'translatedSentences': 0,
            'predictionScore': 0,
            'translationTime': 0
        },
        "message": "data retrieved successfully"
    }

    # # Start counting translation time
    start = time()


    # Get text, src, tgt from input request
    text = request.json.get('text')
    src = request.json.get('sourceLanguageCode')
    tgt = request.json.get('targetLanguageCode')
    # # Split sentences using nltk library ('nltk_data' directory needed, located at home)
    sentences = sent_tokenize(text)
    final_text = ""
    length_senteces = len(sentences)
    list_of_sentences = []
    # for sentence in sentences:

    #     list_of_sentences.append(get_translated_sentence(sentence, src, tgt))
    list_of_sentences = get_translated_sentence(sentences, src, tgt)
    # executor = concurrent.futures.ProcessPoolExecutor(5)
    # translated_sentece = [executor.submit(get_translated_sentence, item,src,tgt) for item in sentences]
    # concurrent.futures.wait(translated_sentece)
    # print(translated_sentece)
    # for item in translated_sentece:
    #     final_text = final_text +" "+ item.result()
    
    
    # list_of_sentences = [n.result() for n in translated_sentece]
    
    # with concurrent.futures.ProcessPoolExecutor(10) as executor:
    #    for sentence in sentences:
    #       future=executor.submit(get_translated_sentence, sentence,src,tgt)
    #       list_of_sentences.append(future.result())

    # print(list_of_sentences)
    final_text = " ".join(list_of_sentences)

    # with open("/home/data/log.txt",'r') as doc:
    #     text = doc.readlines()
    #     text = text[1]
    #     splitted = text.split(" ")[6]

    end = time()
    translation_time = end - start
    reponse['data']['translationTime'] = translation_time
    reponse['data']['sourceLanguage'] = src
    reponse['data']['targetLanguage'] = tgt
    reponse['data']['originalText'] = text
    reponse['data']['translation'] = final_text
    reponse['data']['predictionScore'] = 0
    reponse['data']['translatedSentences'] = list_of_sentences

    
    
    # # Start counting translation time
    # start = time()

    # # For each sentence call OpenNMT API
    # translated_sentences = []
    # pred_scores = []
    # for sentence in sentences:
    #     opennmt_response = translate_sentence(src, tgt, sentence)
    #     print(opennmt_response)
    #     # Because opennmt returns a list of list of dict, we access the [0][0] element
    #     translated_sentence_dict = opennmt_response.json()[0][0]

    #     # 'tgt' and 'pred_score' keys are defined in OpenNMT API
    #     translated_sentence = translated_sentence_dict.get('tgt')
    #     pred_score = translated_sentence_dict.get('pred_score')

    #     # Append translated sentence and prediction score to their respective lists
    #     translated_sentences.append(translated_sentence)
    #     pred_scores.append(pred_score)

    # # Calculate the translation time
    # end = time()
    # translation_time = end - start

    # # Calculate the average prediction score among all sentences translation
    # avg_pred_score = mean(pred_scores)

    # # Prepare the data object
    # data = {
    #     'sourceLanguage': src,
    #     'targetLanguage': tgt,
    #     'originalText': text,
    #     'translatedSentences': translated_sentences,
    #     'predictionScore': avg_pred_score,
    #     'translationTime': translation_time
    # }

    # Convert data to response format and return it as a valid JSON
    return jsonify(reponse)
