#!/bin/bash

# This file tokenizes an input file to be translated
# Inputs:
#		-d : Data directory where the SentencePiece models and translation models are stored
#		-s : Language of the source file. Valid options are: en, es, or pt
#		-t : Language of the target file. Valid options are: en, es, or pt
#		-f : Path to the file that will be translated

while getopts d:s:t:f: option

do
case "${option}"
in
d) DATA=${OPTARG};;
s) src=${OPTARG};;
t) tgt=${OPTARG};;
f) file_trans=${OPTARG};;
esac
done

#DATA='/data/enpt_es'
#src='en'
#tgt='es'
#file_trans='engTerms_totranslate.txt'

# For Spanish as target


if [[ $tgt = "es" ]]
then
	spm_encode --model=${DATA}/pten_esSP32k.model --output_format=piece < ${file_trans} > ${file_trans}.tok ;
fi

# For English as target
if [[ $tgt = "en" ]]
then
	spm_encode --model=${DATA}/espt_enSP32k.model --output_format=piece < ${file_trans} > ${file_trans}.tok ;
fi

# For Portuguese as target 
if [[ $tgt = "pt" ]]
then
	spm_encode --model=${DATA}/enes_ptSP32k.model --output_format=piece < ${file_trans} > ${file_trans}.tok ;
fi

# Add source and target markers for each line in the tokenized file
perl -i.bak -pe "s//__opt_src_${src} __opt_tgt_${tgt} /" ${file_trans}.tok