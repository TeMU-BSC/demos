FROM tensorflow/tensorflow:2.4.1

#MAINTAINER Jouni Luoma "jouni.a.luoma@utu.fi"
# Copies the code inside the container

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
RUN /usr/bin/python3 -m pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
# Defines train.py as script entrypoint

#ENV PYTHONBUFFERED=TRUE
#ENV PATH="/app:${PATH}"
COPY . /app
# ENTRYPOINT [ "python3" ]
# CMD [ "tag-ner.py" ]

#EXPOSE 5000