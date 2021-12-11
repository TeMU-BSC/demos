'''
Module that makes HTTP requests to the OpenNMT API:
http://forum.opennmt.net/t/simple-opennmt-py-rest-server/1392
'''

import json
import requests

# TODO change this URL when Felipe has migrated it to other virtual machine.
URL = 'http://bsccnio01.bsc.es:5000/translator/translate'

# Integers defined by the OpenNMT API depending on the target language.
MODEL = {
    'es': 100,
    'en': 200,
    'pt': 300,
}


def translate_sentence(src: str, tgt: str, sentence: str) -> dict:
    '''
    Translates a single sentence, passing the appropiate headers and data,
    which is a list that contains an object (dict) with the keys 'src'
    (string) and 'model' (integer).

    Example of data content:
    [
        {
            "src": "__opt_src_en __opt_tgt_es This is an example sentence to be translated.",
            "id": 100
        }
    ]

    Example of a complete HTTP request using curl in Terminal:
    curl -i -X POST -H "Content-Type: application/json" 
        -d '[{"src": "__opt_src_en __opt_tgt_es This is an example sentence to be translated.", "id": 100}]'
        http://bsccnio01.bsc.es:5000/translator/translate
    '''
    headers = {
        'Content-Type': 'application/json',
    }
    data = [
        {
            'src': f'__opt_src_{src} __opt_tgt_{tgt} {sentence}',
            'id': MODEL.get(tgt)
        }
    ]
    print("Esto es data")
    print(data)
    return requests.post(URL, headers=headers, data=json.dumps(data))
