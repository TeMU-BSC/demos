
from os import environ, path, walk
from statistics import mean
from time import time
from typing import Dict, List

from flask import g, json, request, jsonify
from flask_cors import CORS

from app import app

CORS(app)


@app.route('/hello', methods=['POST'])
def hello():
    return jsonify(request.json.get("INPUTTEXT")+"Respuesta")
