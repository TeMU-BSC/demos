FROM python:3.7
# FROM ubuntu:18.04

# Defining working directory and adding source code
WORKDIR /app
COPY . .

# Install API dependencies
# RUN apt install -y python3 python-pip
# RUN pip install pipenv
# RUN pipenv install
# RUN pipenv shell
# RUN pipenv lock --requirements > requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

# Start app
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD flask run
