'''
Main python script that runs the Flask app.

Author:
    Alejandro Asensio
    https://github.com/aasensios
'''

from os import path, walk
from statistics import mean
from time import time
from typing import Dict, List
from flask import Flask, g, request, jsonify
from flask_cors import CORS
from nltk import sent_tokenize

import opennmt_caller

# To run in debug mode
# https://stackoverflow.com/questions/52162882/set-flask-environment-to-development-mode-as-default/52164534
# from dotenv import load_dotenv

APP = Flask(__name__)
CORS(APP)
SAMPLES_DIR = 'samples/'

# ----------------------------------------------------------------------------


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

# ----------------------------------------------------------------------------


@APP.route('/samples', methods=['GET'])
def get_samples():
    '''
    Get all text samples inside './samples/' directory.
    Returns a list of filenames and their respective content in a JSON format.
    '''
    samples = []
    for root, dirs, files in walk(SAMPLES_DIR):
        # print(root, dirs, files)
        for filename in files:
            # The two last letters describe the language
            lang_dir = root[-2:]
            # Read the content of each file
            with open(path.join(root, filename), 'r') as current_file:
                content = current_file.read()
            # Append an object for each file
            samples.append({
                'language': lang_dir,
                'filename': filename,
                'content': content
            })
    return jsonify(convert_data_to_response(samples))


# ----------------------------------------------------------------------------


@APP.route('/translate', methods=['POST'])
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
    # Get text, src, tgt from input request
    text = request.json.get('text')
    src = request.json.get('sourceLanguageCode')
    tgt = request.json.get('targetLanguageCode')

    # Split sentences using nltk library ('nltk_data' directory needed, located at home)
    sentences = sent_tokenize(text)

    # Start counting translation time
    start = time()

    # For each sentence call OpenNMT API
    translated_sentences = []
    pred_scores = []
    for sentence in sentences:
        opennmt_response = opennmt_caller.translate_sentence(
            src, tgt, sentence)

        # Because opennmt returns a list of list of dict, we access the [0][0] element
        translated_sentence_dict = opennmt_response.json()[0][0]

        # 'tgt' and 'pred_score' keys are defined in OpenNMT API
        translated_sentence = translated_sentence_dict.get('tgt')
        pred_score = translated_sentence_dict.get('pred_score')

        # Append translated sentence and prediction score to their respective lists
        translated_sentences.append(translated_sentence)
        pred_scores.append(pred_score)

    # Calculate the translation time
    end = time()
    translation_time = end - start

    # Calculate the average prediction score among all sentences translation
    avg_pred_score = mean(pred_scores)

    # Prepare the data object
    data = {
        'sourceLanguage': src,
        'targetLanguage': tgt,
        'originalText': text,
        'translatedSentences': translated_sentences,
        'predictionScore': avg_pred_score,
        'translationTime': translation_time
    }

    # Convert data to response format and return it as a valid JSON
    return jsonify(convert_data_to_response(data))


# ----------------------------------------------------------------------------

if __name__ == "__main__":
    # APP.run()
    APP.run(host='0.0.0.0', port=5001, debug=True)
