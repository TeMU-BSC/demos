# https://docs.docker.com/compose/gettingstarted/

FROM python:3.7-alpine

# Copy necessary files for "nltk" python package
COPY nltk_data /usr/local/nltk_data

WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]