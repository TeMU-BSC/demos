#!/usr/bin/env python
import re, csv, os


# Funciones para
# Cargar terminologías (taken from TEMUNormalizer)
def loadDict(filepath):
    """Function to load the tsv files containing the ontologies in code format. The function will read these terms
     and will return a dictionary in which the key will be the string of the term and the value a list with 

    Args:
        filepath ([str]): Path to the tsv folder.

    Returns:
        [dict]: Dictionary in which the keys correspond to terms of an ontology and the values to the assigned code.
    """
    # Remove brackets from descriptions
    r = re.compile(r'\(.*\)$')
    reference_dict = {}
    for duplo in csv.reader(open(filepath),dialect='excel',delimiter="\t"):
        code = duplo[0]
        term = duplo[1]
        # Remove extra spaces
        term = r.sub('',term).rstrip()
        # Separate codes in case there are two codes for a string (separated by |)
        codes = code.split("|")
        # If term is in reference dict, add code as a list of codes
        if term in reference_dict.keys():
            previous_codes = reference_dict[term]
            newlist = list(set(codes).union(set(previous_codes)))
            reference_dict[term] = newlist
        else: 
            reference_dict[term.strip()] = codes
    print("Loaded dictionary from: ",filepath)
    print(len(reference_dict)," entries")
    return reference_dict

# Load termlist
def loadTermList(apath):
    """Load a list of terms to normalize

    Args:
        apath ([str]): Path to the terms file

    Returns:
        [list]: list of terms to normalize
    """
    termlist = list()
    with open(apath,'r', encoding='utf-8') as f:
        for term in f.readlines():
            termlist.append(term.strip())
    print("Loaded term list from: ",apath)
    print(len(termlist)," terms")
    return termlist

def loadAnn(apath,entidades=None):
    """
    Parameters
    ----------
    apath : TYPE
        DESCRIPTION.
    entidades : TYPE, optional
        DESCRIPTION. The default is [].

    Returns
    -------
    termlist : TYPE
        DESCRIPTION.
        
    """
    termlist = list()
    for line in csv.reader(open(apath),dialect='excel',delimiter="\t"):
        if entidades:
            if line[1].split(" ")[0] in entidades:
                termlist.append(line[-1])
        else:
                termlist.append(line[-1])
    return termlist


def notEmpty(termdic):
    termlist = []
    for t in termdic:
        if termdic[t] == '':
            termlist.append(t)
    return termlist

# Cargar texto (sin hacerlo lowercase)


# Get llist of input files
def get_input_files(input_path, is_ann):
        """Function to get the list of files with terms to be annotated

        Args:
            options ([type]): [description]

        Returns:
            [type]: [description]
        """
        dirin = input_path
        # Get paths of all files
        
        if dirin[-1] != os.path.sep:
            dirin = dirin+os.path.sep
        if is_ann:
            filesin = [f for f in os.listdir(dirin) if f.endswith('.ann')]
        else:
            filesin = os.listdir(dirin)
        return filesin