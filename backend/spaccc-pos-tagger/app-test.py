'''
Main python script that runs the Flask app.

Author:
    Alejandro Asensio
    https://github.com/aasensios
'''

from os import path, walk
from flask import Flask, request, jsonify
from flask_cors import CORS
from med_tagger import Med_Tagger/Med_Tagger

APP = Flask(__name__)
CORS(APP)
# CORS(APP, resources={r'/*': {'origins': '*'}})
MED_TAGGER = MedTagger()
# APP.config['CORS_HEADERS'] = 'Content-Type'

# https://freeling-user-manual.readthedocs.io/en/latest/tagsets/tagset-es/
POS = {
    'A': 'adjective',
    'C': 'conjunction',
    'D': 'determiner',
    'N': 'noun',
    'P': 'pronoun',
    'R': 'adverb',
    'S': 'adposition',
    'V': 'verb',
    'Z': 'number',
    'W': 'date',
    'I': 'interjection',
    'F': 'punctuation'
}

# ----------------------------------------------------------------------------


def convert_med_tagger_result_to_data(parsed_text: List[List]) -> Dict:
    '''
    Convert a given parsed text in a List of lists format, into a dictionary
    that contains sentences, and those sentences contain its respective words
    (parts of speech).
    '''
    # Prepare the result dict.
    result = {
        'sentenceCount': len(parsed_text),
        'sentences': [],
    }
    word_id_in_text = 0
    # Get the sentences of the text.
    for sentence_id, parsed_sentence in enumerate(parsed_text):
        # Convert each sentence into a key-value dictionary and append its words to that dict.
        sentence = {
            'id': sentence_id + 1,  # natural counting starting at 1
            'wordCount': len(parsed_sentence),
            'words': [],
        }
        # Get the words of the sentence.
        for word_id_in_sentence, parsed_word in enumerate(parsed_sentence):
            # Delete the newline character from the score and convert it to number.
            score = float(parsed_word[3].strip())
            # Get the word (word or punctuation mark).
            word = {
                'id': word_id_in_text + 1,  # natural counting starting at 1
                'forma': parsed_word[0],
                'lemma':  parsed_word[1],
                'tag':  parsed_word[2],
                'pos':  POS.get(parsed_word[2][0]),
                'score': score,
            }
            sentence.get('words').append(word)
            word_id_in_text += 1
        result.get('sentences').append(sentence)
    return result

# ----------------------------------------------------------------------------


def convert_to_api_response(data: Dict) -> Dict:
    '''
    Prepare the API result skeleton.
    '''
    api_response = {
        'success': True,
        'data': data,
        'message': 'Data retrieved successfully.'
    }
    return api_response

# ----------------------------------------------------------------------------


@APP.route('/samples', methods=['GET'])
def get_samples():
    '''
    Get all text samples inside './samples/' directory.
    Returns a list of filenames and their respective content in a JSON format.
    '''
    result = []
    for root, dirs, files in walk('./samples/'):
        for filename in files:
            with open(path.join(root, filename), 'r') as current_file:
                content = current_file.read()
            result.append({
                'filename': filename,
                'content': content
            })
    return jsonify(convert_to_api_response(result))

# ----------------------------------------------------------------------------


@APP.route('/analyze', methods=['POST'])
def analyze():
    '''
    Get all medical tags. Parses the input medicalReport and outputs a
    dictionary with all possible medical tags and scores.
    '''
    text = request.json.get('medicalReport')
    parsed_text = MED_TAGGER.parse(text)
    if not any(isinstance(el, list) for el in parsed_text):
        parsed_text = [parsed_text]
    result = convert_med_tagger_result_to_data(parsed_text)
    return jsonify(convert_to_api_response(result))

# ----------------------------------------------------------------------------


@APP.route('/')
def index():
    '''
    Dummy root route for testing.
    '''
    return 'Hello from Flask!'


if __name__ == "__main__":
    # APP.run()
    APP.run(host='0.0.0.0', port=5000)
