#!/bin/bash

# This file translate file
# Inputs:
#		-l : Target Language


while getopts l: option

do
case "${option}"
in
l) l=${OPTARG};;
esac
done

#For Spanish as target
if [[ $l = "es" ]]
then
	python3 OpenNMT-py/translate.py -model /app/data/pten_es_model.pt -gpu -1 -src /home/data/text.txt.tok -replace_unk -output /home/data/text.translated ;
    spm_decode --model=/app/data/pten_esSP32k.model < /home/data/text.translated > /home/data/text.translated.detokenized;
fi

# For English as target
if [[ $l = "en" ]]
then
	python3 OpenNMT-py/translate.py -model /app/data/espt_en_model.pt -gpu -1 -src /home/data/text.txt.tok -replace_unk -output /home/data/text.translated ;
    spm_decode --model=/app/data/espt_enSP32k.model < /home/data/text.translated > /home/data/text.translated.detokenized;
fi

# For Portuguese as target 
if [[ $l = "pt" ]]
then
	python3 OpenNMT-py/translate.py -model /app/data/enes_pt_model.pt -gpu -1 -src /home/data/text.txt.tok -replace_unk -output /home/data/text.translated ;
    spm_decode --model=/app/data/enes_ptSP32k.model < /home/data/text.translated > /home/data/text.translated.detokenized;
fi



