# -*- coding: utf-8 -*-
"""
Spyder Editor

Brat to BIOES
"""
import os
import glob
from . import brat_to_conll
from . import conll_to_brat
from . import general_utils
from . import utils_nlp

def _get_valid_dataset_filepaths(dataset_text_folder, tokenizer, spacylanguage, tagging_format,
                                 dataset_types=['train', 'valid', 'test', 'deploy']):
    dataset_filepaths = {}
    dataset_brat_folders = {}
    for dataset_type in dataset_types:
        dataset_filepaths[dataset_type] = os.path.join(dataset_text_folder, '{0}.txt'.format(dataset_type))
        dataset_brat_folders[dataset_type] = os.path.join(dataset_text_folder, dataset_type)
        dataset_compatible_with_brat_filepath = os.path.join(dataset_text_folder, '{0}_compatible_with_brat.txt'.format(dataset_type))

        # Conll file exists
        if os.path.isfile(dataset_filepaths[dataset_type]) and os.path.getsize(dataset_filepaths[dataset_type]) > 0:
            # Brat text files exist
            if os.path.exists(dataset_brat_folders[dataset_type]) and len(glob.glob(os.path.join(dataset_brat_folders[dataset_type], '*.txt'))) > 0:

                # Check compatibility between conll and brat files
                brat_to_conll.check_brat_annotation_and_text_compatibility(dataset_brat_folders[dataset_type])
                if os.path.exists(dataset_compatible_with_brat_filepath):
                    dataset_filepaths[dataset_type] = dataset_compatible_with_brat_filepath
                conll_to_brat.check_compatibility_between_conll_and_brat_text(dataset_filepaths[dataset_type], dataset_brat_folders[dataset_type])

            # Brat text files do not exist
            else:

                # Populate brat text and annotation files based on conll file
                conll_to_brat.conll_to_brat(dataset_filepaths[dataset_type], dataset_compatible_with_brat_filepath, dataset_brat_folders[dataset_type], dataset_brat_folders[dataset_type])
                dataset_filepaths[dataset_type] = dataset_compatible_with_brat_filepath

        # Conll file does not exist
        else:
            # Brat text files exist
            if os.path.exists(dataset_brat_folders[dataset_type]) and len(glob.glob(os.path.join(dataset_brat_folders[dataset_type], '*.txt'))) > 0:
                dataset_filepath_for_tokenizer = os.path.join(dataset_text_folder, '{0}_{1}.txt'.format(dataset_type, tokenizer))

                if os.path.exists(dataset_filepath_for_tokenizer):
                    conll_to_brat.check_compatibility_between_conll_and_brat_text(dataset_filepath_for_tokenizer, dataset_brat_folders[dataset_type])
                else:
                    # Populate conll file based on brat files
                    brat_to_conll.brat_to_conll(dataset_brat_folders[dataset_type], dataset_filepath_for_tokenizer, tokenizer, spacylanguage)
                dataset_filepaths[dataset_type] = dataset_filepath_for_tokenizer

            # Brat text files do not exist
            else:
                del dataset_filepaths[dataset_type]
                del dataset_brat_folders[dataset_type]
                continue

        if tagging_format == 'bioes':
            # Generate conll file with BIOES format
            bioes_filepath = os.path.join(dataset_text_folder, '{0}_bioes.txt'.format(general_utils.get_basename_without_extension(dataset_filepaths[dataset_type])))
            utils_nlp.convert_conll_from_bio_to_bioes(dataset_filepaths[dataset_type], bioes_filepath)
            dataset_filepaths[dataset_type] = bioes_filepath

    return dataset_filepaths, dataset_brat_folders