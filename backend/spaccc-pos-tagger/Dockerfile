# https://docs.docker.com/compose/gettingstarted/

FROM python:3.7-alpine

# Copy necessary files for "nltk" python package
COPY nltk_data /usr/local/nltk_data

WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
CMD ["flask", "run"]


# -----------------------------------------------------------------------------
FROM ubuntu:18.04

# Defining working directory and adding source code
WORKDIR /code
COPY . .

# If docker starts FROM ubuntu, install python and pip
RUN apt-get install -y python3 python-pip
RUN pip install --user -U pipenv
RUN pipenv install
RUN pipenv shell
# RUN pipenv lock --requirements > requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -r requirements.txt

# Start app
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
CMD flask run
