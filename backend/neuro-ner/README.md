# Custom NCRFpp adapted to TeMU use case
Basically, I have added support to input and output Brat files in decode mode and made support for pretrained model on CPU.

## Prerequisites
torch==1.2.0+cpu 
torchvision==0.4.0+cpu
spacy=2.0.18
es_core_news_sm spacy model

## Installation 

### Prerequisites
```
python3 -m venv test
source test/bin/activate
pip install torch==1.2.0+cpu torchvision==0.4.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install spacy==2.0.18
python -m spacy download es_core_news_sm
```

### Library
```
git clone https://github.com/tonifuc3m/testing-negation-rbbt.git
```

# Usage

```
cd testing-negation-rbbt
python -W ignore main.py --config demo.decode.config
```


