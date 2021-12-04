#!/usr/bin/env python

import unicodedata


# Limpieza de texto de distinto tipo (stopwords, stemming, lematizacion, lowerfcase). Limpiar tanto las terminologías como los términos
def preprocessing_dict(selected_preprocessing_steps, reference_dict,stopwords, stemmer):
    """Function to preprocess dictionary with ontology terms

    Args:
        selected_preprocessing_steps ([list]): list of strings indicating the preprocessing steps to carry out.
        reference_dict ([dict]): [description]
        stopwords ([list]): [description]
        stemmer ([Stemmer object (nltk)]): [description]

    Returns:
        [dict]: dict with terms preprocessed
    """
    list_keys = list(reference_dict.keys())
    list_values = list(reference_dict.values())
    list_keys_final = list_keys.copy()
    for i in selected_preprocessing_steps:
            if i == "lowercase":
                print("Lowercasing terms...")
                list_keys_final = lowercase(list_keys_final)
            elif i == "stopwords":
                print("Removing stopwords...")
                list_keys_final = remove_stopwords(list_keys_final,stopwords)
            elif i == "stemming":
                print("Stemming terms...")
                list_keys_final = stemming(list_keys_final, stemmer)
            elif i == "lematization":
                print("lematization")
            elif i == "accents":
                print("Normalizing accents...")
                list_keys_final = strip_accents(list_keys_final)
            else:
                print("Preprocessing step not available")
    reference_dict = dict(zip(list_keys_final,list_values))
    return reference_dict

def preprocessing_list(selected_preprocessing_steps, termlist, stopwords,stemmer):
    """[summary]

    Args:
        selected_preprocessing_steps ([list]): list of strings indicating the preprocessing steps to carry out.
        termlist ([list]): List of terms to be preprocessed before normalising
        stopwords ([list]): [description]
        stemmer ([Stemmer object (nltk)]): [description]

    Returns:
        [list]: list with terms preprocessed
    """
    list_keys_final = termlist.copy()
    for i in selected_preprocessing_steps:
            if i == "lowercase":
                print("Lowercasing terms...")
                list_keys_final = lowercase(list_keys_final)
            elif i == "stopwords":
                print("Removing stopwords...")
                list_keys_final = remove_stopwords(list_keys_final,stopwords)
            elif i == "stemming":
                print("Stemming terms...")
                list_keys_final = stemming(list_keys_final, stemmer)
            elif i == "lematization":
                print("lematization")
            elif i == "accents":
                print("Normalizing accents...")
                list_keys_final = strip_accents(list_keys_final)
            else:
                print("The preprocessing step called {} does not exist.".format(i))
    
    return list_keys_final

# Funcion remove lowercase
def lowercase(lista):
    """Function to lowercase list of texts

    Args:
        lista ([list]): list of texts

    Returns:
        [list]: List of texts lowercased
    """
    return [text.lower() for text in lista]
# Funccion remove stopwords
def remove_stopwords(lista,stopwords):
    """Function to remove stopwords

    Args:
        lista ([list]): list of texts
        stopwords ([list]): [description]

    Returns:
        [list]: List of texts without stopwords
    """
    lista_out = list()
    for idx, text in enumerate(lista):
        text = ' '.join([word for word in text.split() if word not in stopwords])
        text = text.strip()
        lista_out.append(text)
    #print("Len original: {} - Len processed stopwords: {}".format(len(lista),len(lista_out)))
    return lista_out
# Funcion stemming
def stemming(lista, stemmer):
    """Function to stem tokens coming from a list of texts

    Args:
        lista ([list]): list of texts
        stemmer ([type]): Stemmer object
    Returns:
        [type]: [description]
    """
    lista_out = list()
    for text in lista:
         lista_out.append(' '.join([stemmer.stem(word) for word in text.split()]))
    return lista_out
# Strip accents (from https://stackoverflow.com/a/31607735 )
def strip_accents(lista):
    """Function to normalize accents (removing them)

    Args:
        lista ([list]): list of texts

    Returns:
        [type]: [description]
    """
    lista_out = list()
    for idx,text in enumerate(lista):
        try:
            text = unicode(text, 'utf-8')
        except (TypeError, NameError): # unicode is a default on python 3 
            pass
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
        lista_out.append(str(text))
    return lista_out
