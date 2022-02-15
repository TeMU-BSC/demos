# Use an official python image
FROM python:3.7

# Set the working directory to /app
WORKDIR /app

# COPY tensorflow-2.5.0-cp38-cp38-linux_x86_64.whl .
# copy the dependencies file to the working directory
COPY requirements.txt .

# RUN pip3 install -U tensorflow-2.5.0-cp38-cp38-linux_x86_64.whl
# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m spacy download es_core_news_sm
RUN apt-get update -y 
RUN apt-get -y install \
  bison autoconf g++ libxslt1-dev make \
  zlib1g-dev libbz2-dev libreadline-dev \
  wget curl git openssl libyaml-0-2 libyaml-dev \
  openjdk-11-jdk \
  libcairo2 libcairo2-dev r-base-core r-base-dev r-cran-rserve liblzma5 liblzma-dev libcurl4-openssl-dev \
  build-essential zlib1g-dev libssl-dev libyaml-dev libffi-dev ruby-dev ruby-tokyocabinet
RUN gem install --no-force --force rbbt-util rbbt-rest rbbt-dm rbbt-sources  rbbt-text
# Copy the current directory contents into the container at /app 
COPY . /app
WORKDIR /app

# Copy necessary files for "nltk" python package into one of these directories inside container:
#   - '/root/nltk_data'
#   - '/usr/local/nltk_data'
#   - '/usr/local/share/nltk_data'
#   - '/usr/local/lib/nltk_data'
#   - '/usr/share/nltk_data'
#   - '/usr/local/share/nltk_data'
#   - '/usr/lib/nltk_data'
#   - '/usr/local/lib/nltk_data'
#   - ''
# COPY nltk_data /usr/local/nltk_data
