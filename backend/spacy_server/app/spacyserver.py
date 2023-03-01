from ast import Global
import os
import sys
import unicodedata
import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package]) 


from flask_cors import CORS,cross_origin
from flask import Flask, request
from app import app
import_or_install("numpy")
import_or_install("pandas")
import numpy as np
from flask import g, json, request, jsonify
import spacy
from spacy import displacy
from spacy.tokens import Span
import pandas as pd


     

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


HPO = pd.read_csv("HPO_es_master_20220611_v0_updatedfrom220214 - HPO_es_master_20220611_v0_updatedfrom220214.tsv",sep="\t")
HPO.drop(labels=["syn_type","syn_id","source","branch_1","branch_2","branch_3","branch_4","branch_5"],axis=1,inplace=True)
HPO_DIC = []


for n in range(1,len(HPO)):
    if pd.isna(HPO.iloc[n,7]) !=True and HPO.iloc[n,5] in (["label","synonym"]):
        aux_dic = {}
        aux_dic["label"] = "HPO"
        aux_dic["id"] = HPO.iloc[n,1]
        text = HPO.iloc[n,7]
        text = text.split(" ")
        pats = []
        for word in text:
            pats.append({"LEMMA":normalize(word.lower())})
        aux_dic["pattern"] = pats
        HPO_DIC.append(aux_dic)

        if pd.isna(HPO.iloc[n,6]) != True:
            text = HPO.iloc[n,6]
            text = text.split(" ")
            pats = []
            for word in text:
                pats.append({"LEMMA":normalize(word.lower())})
            aux_dic["pattern"] = pats
            HPO_DIC.append(aux_dic)


hpo_model = spacy.load("es_core_news_sm")
ruler  = hpo_model.add_pipe("entity_ruler")
patterns = HPO_DIC
with hpo_model.select_pipes(enable="tagger"):
    ruler.add_patterns(patterns)


CORS(app)
global models
models = {}
models["HPO"] = hpo_model
def loadmodels(name):
    if name in models.keys():
        return models[name]
    else:
        nlp = spacy.load("/spacy_models/"+name)
        #nlp.tokenizer = custom_tokenizer(nlp)
        models[name] = nlp
        return models[name]
    

from spacy.symbols import ORTH
from spacy.tokenizer import Tokenizer
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS,PUNCT
from spacy.util import compile_infix_regex, compile_suffix_regex
import re 

#Create a custom tokenizer for spanish language spacy model


from tqdm import tqdm
from spacy.tokens import DocBin
from spacy.symbols import ORTH
from spacy.tokenizer import Tokenizer
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex, compile_suffix_regex


    

@app.route('/spacy_server', methods=['GET'])
def prueba():
    return "Hola funciona"

@app.route('/get_model_info', methods=['GET'])
def get_model_info():
    with open("/spacy_models/models_info.json") as json_file:
        data = json.load(json_file)
    return jsonify(data)

@app.route("/get_all_ner_annotations",methods=['POST'])
def get_all_ner_nnotations():
    data = request.get_json()
    model_names = data['MODEL']
    print("modelos nombres")
    print(data)
    text = data['INPUTTEXT']
    nlp_aux = loadmodels(model_names[0])
    doc_aux = nlp_aux(text)
    for model_name  in model_names:
        nlp = loadmodels(model_name)
        doc = nlp(text)
        ents = []
        for ent in doc.ents:
            ents.append(Span(doc, ent.start, ent.end, label=ent.label_))
        doc_aux.spans["sc"] = doc_aux.spans["sc"] + ents
    return jsonify({"html" : displacy.render(doc_aux, style="span")})


@app.route("/get_annotations", methods=['POST'])
def get_prediction():
    json_input = request.json
    text = json_input['INPUTTEXT'].rstrip()
    model = json_input['MODEL']
    nlp = loadmodels(model)
    doc = nlp(text)
    output = []
    n = 0
    model_info = {}
    with open("/spacy_models/models_info.json") as json_file:
        model_json_data = json.load(json_file)
        for model_data in model_json_data:
            if model_data['route'] == model:
                model_info = model_data
                break

    options = {"ents": model_info['entities'], "colors": model_info['colors']}
    for ent in doc.ents:
        dic = {
        "A-ID":"T"+str(n),
        "B-TYPE": ent.label_,
        "C-START": ent.start_char,
        "D-END": ent.end_char,
        "E-text": ent.text,
         }
        output.append(dic)
        n += 1
    return jsonify({"INPUTTEXT":output,"html" : displacy.render(doc, style="ent", options=options)})


@app.route("/get_phenotype_annotations", methods=['POST'])
def get_phenotype_annotations():
    json_input = request.json
    text = json_input['INPUTTEXT'].rstrip()
    models = ["Phenotypes_1","Phenotypes_2","HPO"]
    n = 0
    output = []
    
    for model in models:
        nlp = loadmodels(model)
        doc = nlp(normalize(text.lower()))

        
        for ent in doc.ents:
            if ent.label_ not in ["LOC","MISC","PER","ORG"]:
                if ent.label_ == "HPO":
                    dic = {
                    "A-ID":"T"+str(n),
                    "B-TYPE": "HPO",
                    "C-START": ent.start_char,
                    "D-END": ent.end_char,
                    "E-text":text[ent.start_char:ent.end_char].lower(),
                    "F-HPO": ent.ent_id_,
                    }
                if ent.label_ == "ENFERMEDAD_ph":
                    dic = {
                    "A-ID":"T"+str(n),
                    "B-TYPE": "DISEASE",
                    "C-START": ent.start_char,
                    "D-END": ent.end_char,
                    "E-text":text[ent.start_char:ent.end_char].lower(),
                    
                    }

                if ent.label_ == "SINTOMA_ph":
                    dic = {
                    "A-ID":"T"+str(n),
                    "B-TYPE": "SYMPTOM",
                    "C-START": ent.start_char,
                    "D-END": ent.end_char,
                    "E-text":text[ent.start_char:ent.end_char].lower(),
                    }
                if ent.label_ == "PHENOTYPE":
                     dic = {
                    "A-ID":"T"+str(n),
                    "B-TYPE": ent.label_,
                    "C-START": ent.start_char,
                    "D-END": ent.end_char,
                    "E-text": text[ent.start_char:ent.end_char].lower(),
                    }
                output.append(dic)
                n += 1

    #create table from output  
    Datos = pd.DataFrame(data=output,columns=["B-TYPE","E-text"])
    Datos.loc[Datos["B-TYPE"].isin(["DISEASE","SYMPTOM"]),"B-TYPE"] = "PHENOTYPE_2" 
    Datos2 = pd.DataFrame(Datos.groupby(by=["E-text","B-TYPE"])["B-TYPE"].count()).rename(columns={"B-TYPE": "count"}).reset_index()
    Datos2 = Datos2.pivot_table("count",["E-text"],"B-TYPE").fillna(0).astype(int)
    table = Datos2.reset_index().to_dict(orient="record")
    return jsonify({"INPUTTEXT":output,"TABLE":table})




# @app.route('/get_annotations', methods=['POST'])
# def tag():
#     json_input = request.json
#     text = json_input['INPUTTEXT'].rstrip()
#     model = json_input['MODEL']
#     print("tagging")
#     if model == "chemical":
#         return app.tagger_chemical.tag(text)
#     elif model == "gene":
#         return app.tagger_gene.tag(text)
#     else:
#         return "Model not found"
    
#     # #tokenized = request.values.get('tokenized') in ('1', 'True', 'true')
#     # return app.tagger.tag(text) #, tokenized)

# @app.route('/')
# def hello():
#     return "Hello World!"



# def reconstruct_brat(json_path, outpath, conll_file):
#     """

#     Parameters
#     ----------
#     json_path : string
#         Path to input JSON data. I need to to find the path to the Brat folder that was created inside the preprocessing function.
#     outpath : string
#         Path to folder where I will create my output
#     conll_file : string
#         Path to .BIO file created in the previous step.
#     Returns
#     -------
#     None.
#     """
#     # Darryl: inside the preprocessing function, I converted the input files from JSON into Brat format and store them.
#     # Darryl: the function conll_to_brat() needs to look at those Brat format files.
#     brat_original_folder_test = os.path.join(
#         os.path.dirname(json_path), 'brat')

#     # Darryl: Output folder where you want to store your Brat files
#     brat_output_folder_test = outpath

#     # Darryl: In our case, this is the same as path to .BIO file created in the previous step
#     conll_output_filepath_test = conll_file

#     conll_to_brat(conll_file, conll_output_filepath_test,
#                   brat_original_folder_test, brat_output_folder_test, overwrite=True)



# class Tagger(object):
#     def __init__(self, model, tokenizer, labels, config):
#         self.model = model
#         self.tokenizer = tokenizer
#         self.labels = labels
#         self.config = config
#         #self.session = None
#         #self.graph = None

#     def tag(self, text, tokenized=False):
#         max_seq_len = self.config['max_seq_length']
#         inv_label_map = { i: l for i, l in enumerate(self.labels) }
#         if tokenized:
#             words = text.split()    # whitespace tokenization
#         else:
#             words = tokenize(text)    # approximate BasicTokenizer
#         dummy = ['O'] * len(words)
#         data = process_sentences([words], [dummy], self.tokenizer, max_seq_len)
#         x = encode(data.combined_tokens, self.tokenizer, max_seq_len)
#         #if self.session is None or self.graph is None:
#         probs = self.model.predict(x, batch_size=8)    # assume singlethreaded
#         #else:
#         #    with self.session.as_default():
#         #        with self.graph.as_default():
#         #            probs = self.model.predict(x, batch_size=8)
#         preds = np.argmax(probs, axis=-1)
#         pred_labels = []
#         for i, pred in enumerate(preds):
#             pred_labels.append([inv_label_map[t]
#                                 for t in pred[1:len(data.tokens[i])+1]])
#         lines, _ = write_result(
#             'output.tsv', data.words, data.lengths,
#             data.tokens, data.labels, pred_labels, mode='predict'
#         )
        
#         annotations = conll_to_standoff(text,"".join(lines))
#         anns = [a.to_dict(text) for a in annotations]
#         return jsonify(anns)

#     @classmethod
#     def load(cls, model_dir):
#         # session/graph for multithreading, see https://stackoverflow.com/a/54783311
#         #session = tf.Session()
#         #graph = tf.get_default_graph()
#         #with graph.as_default():
#         #    with session.as_default():
#         print(model_dir)
#         model, tokenizer, labels, config = load_ner_model(model_dir)
#         model.trainable = False
#         model.training = False
#         tagger = cls(model, tokenizer, labels, config)
#         #tagger.session = session
#         #tagger.graph = graph
#         return tagger


# punct_chars = set([
#     chr(i) for i in range(sys.maxunicode)
#     if (unicodedata.category(chr(i)).startswith('P') or
#         ((i >= 33 and i <= 47) or (i >= 58 and i <= 64) or
#          (i >= 91 and i <= 96) or (i >= 123 and i <= 126)))
# ])

# translation_table = str.maketrans({ c: ' '+c+' ' for c in punct_chars })


# def tokenize(text):
#     return text.translate(translation_table).split()

# app.tagger_gene = Tagger.load(DEFAULT_MODEL_DIR_GENE)
# app.tagger_chemical = Tagger.load(DEFAULT_MODEL_DIR_CHEMICAL)

# # def main(argv):
# #     argparser = argument_parser('serve')
# #     args = argparser.parse_args(argv[1:])
# #     if args.ner_model_dir is None:
# #         args.ner_model_dir = DEFAULT_MODEL_DIR
# #     app.tagger = Tagger.load(args.ner_model_dir)
# #     app.run(port=args.port,host='0.0.0.0')
# #     return 0






# # if __name__ == '__main__':
# #     sys.exit(main(sys.argv))