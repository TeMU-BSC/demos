# # Use the Python3.7 image
# FROM python:3.7-stretch

# # Set the working directory to /app
# WORKDIR /app

# # Copy the current directory contents into the container at /app 
# ADD . /app

# # Install the dependencies
# RUN pip install --upgrade pip && \
#     pip install -r requirements.txt


# ***********
FROM ubuntu:18.04
WORKDIR /app
ADD . /app
RUN apt-get update -y && \
    apt-get install -y curl

# https://github.com/docker/docker-install
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh && \
    dockerd

# install python
RUN apt-get install -y python3 python3-pip
RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install -r requirements.txt

# # flask-pos           | This system supports the C.UTF-8 locale which is recommended.
# # flask-pos           | You might be able to resolve your issue by exporting the
# # flask-pos           | following environment variables:
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8


# # ***********
# # Alternative: pipenv
# RUN pip install pipenv
# RUN pipenv install
# RUN pipenv shell
# RUN pipenv lock --requirements > requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -r requirements.txt
