#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 1 12:03:49 2021

@author: luisgasco

"""

import csv, os, sys, pickle
# Include system path
# sys.path.append(os.getcwd()+"/src/baseline/baseline_utils")

from norm_to_darryl.baseline.baseline_utils.preprocessing import preprocessing_dict,preprocessing_list
from norm_to_darryl.baseline.baseline_utils.loaders import loadDict, get_input_files, loadTermList, loadAnn
from norm_to_darryl.baseline.baseline_utils.normalizers import normalize_mention_list
from norm_to_darryl.baseline.baseline_utils.savers import writeOut, saveAnn, prepare_output_path
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import unicodedata, re
from optparse import OptionParser

##########################################################
# Define variables for normalization (input, output, etc)#
##########################################################
reference_dict_path = "norm_to_darryl/ontologies/snomed_ct_spanishgov_edition_onlyactiveterms.tsv"
preprocessing_args = ["lowercase"]
# input_path =  "/mnt/c/Users/bscuser/Documents/spanorm/data/interim/to_normalize/ann_files/many_files/"
# output_path = "/mnt/c/Users/bscuser/Documents/spanorm/data/output/to_normalize/many_files/" 
is_ann = True # True if you want to process brat files (.ann)
is_single_file = False # True if you only want to process one document



#################################################################
# Load constants that will be used in the normalization process #
#################################################################
sw = stopwords.words("spanish")
SStemmer = SnowballStemmer("spanish")
# List of available preprocessings
preprocessing_list_defaults = ["lowercase","stopwords","stemming","lematization","accents"]

############################################################
# Load and preprocess terminological resources (ontologies)#
############################################################
reference_dict = loadDict(reference_dict_path)
reference_dict = preprocessing_dict(preprocessing_args, reference_dict, stopwords=sw, stemmer = SStemmer)

############################################################
# Load and normlaiza texts #################################
############################################################
def get_normalized(input_path,output_path):
    if is_single_file: 
        if is_ann:
            mentionlist = loadAnn(input_path)
            mentionlist = preprocessing_list(preprocessing_args, mentionlist, stopwords = sw, stemmer = SStemmer)
        else:
            # load and preprocess mentions
            mentionlist = loadTermList(input_path)
            mentionlist = preprocessing_list(preprocessing_args, mentionlist, stopwords = sw, stemmer = SStemmer)
        
        # Normalize document
        mentioncodes, meta_dict = normalize_mention_list(mentionlist, reference_dict,input_path)
        
        # Save data
        # Prepare output paths (if only one document is process, the out_file_name will be output_norm)
        out_path, out_file_name = prepare_output_path(output_path, output_path, is_single_file)
        if is_ann:
            saveAnn(input_path, out_path+out_file_name+".ann", mentioncodes)
        else:
            writeOut(mentionlist,mentioncodes,out_path+out_file_name+"_EL.tsv",type=1)
            writeOut(meta_dict,mentioncodes,out_path+out_file_name+"_metadata.tsv",type=2)
    else:
        # Get files to normalize
        filesin = get_input_files(input_path, is_ann)
        # Iterate over the list of files to normalize them
        for file in filesin:
            file_termlist = input_path+file
            # If brat option is selected use loadAnn function
            if is_ann:  
                mentionlist = loadAnn(file_termlist)
                mentionlist = preprocessing_list(preprocessing_args, mentionlist, stopwords = sw, stemmer = SStemmer)
            else:
                mentionlist = loadTermList(file_termlist)
                mentionlist = preprocessing_list(preprocessing_args, mentionlist, stopwords = sw, stemmer = SStemmer)
            # Normalize and save
            mentioncodes, meta_dict = normalize_mention_list(mentionlist, reference_dict, file)
            # Get output files
            out_path, out_file_name = prepare_output_path(output_path, file, is_single_file)
            if is_ann:
                saveAnn(input_path+file, out_path+out_file_name, mentioncodes)
            else:
                writeOut(mentionlist,mentioncodes,out_path+out_file_name+"_EL.tsv",type=1)
                writeOut(meta_dict,mentioncodes,out_path+out_file_name+"_metadata.tsv",type=2)