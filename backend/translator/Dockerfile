# Use an official python image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt install sentencepiece -y && \
    git clone https://github.com/OpenNMT/OpenNMT-py.git && \
    cd OpenNMT-py && \
    python3 setup.py install && \
    pip install -r requirements.opt.txt

# Copy the current directory contents into the container at /app 
COPY /data .
ADD . /app

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
COPY nltk_data /usr/local/nltk_data
