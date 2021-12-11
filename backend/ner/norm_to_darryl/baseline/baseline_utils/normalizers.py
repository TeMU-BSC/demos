#!/usr/bin/env python
import time
# Funcion matching
def lexicalMatch(termlist,reference_dict):
    """function to find lexical match between a list of terms an a reference ontology (reference_dict)

    Args:
        termlist ([type]): [description]
        reference_dict ([type]): [description]

    Returns:
        [type]: [description]
    """
    output_list = list()
    for term in termlist:
        try:
            dictid = reference_dict[term]
            output_list.append([[dictid,100.0]])
        except KeyError:
            # If key is not found, NIL code is assigned
            output_list.append([["NIL",0]])
            pass
    return output_list

def normalize_mention_list(mentionlist, reference_dict, filename):
        # Let's normalize (with baseline the terms)
        print("------------------File:{}-----------------------------".format(filename))
        meta_dict = dict()
        mentioncodes = list()
        # Get number of terms to test
        initiatewith = len(mentionlist)
        # If number of terms is 0, skip this file
        if initiatewith ==0 or len(reference_dict) == 0 :
            print("Skipped file. There are no entities to map.")
            return meta_dict, mentioncodes
        else:
            print("number of terms to test: ", initiatewith)
            t1 = time.time()
            # Number of terms missing after direct mathc:
            print("Trying exact Match")
            mentioncodes = lexicalMatch(mentionlist,reference_dict)
            # Count number of NIL
            nil_count = [elem[0][0] for elem in mentioncodes].count("NIL")
            
            # Calculate percentage of NILs
            percent = (nil_count*100)/initiatewith
            # Calculation Time
            t2 = time.time()
            print(round(100-percent,2),"% of entities found")
            print(" Overall processing in ",(t2-t1)/60," minutes")

            # Assign values to meta_dict
            meta_dict["num_term_test"] = initiatewith 
            meta_dict["num_NIL"] = nil_count
            meta_dict["perc_NIL"] = percent
            meta_dict["perc_match"] = 100-percent
            meta_dict["time_to_compute"] = t2-t1
            return mentioncodes, meta_dict