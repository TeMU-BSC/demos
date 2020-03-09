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
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip curl
RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install -r requirements.txt

# https://github.com/docker/docker-install
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh
# RUN curl -fsSL https://raw.githubusercontent.com/docker/docker-install/master/rootless-install.sh -o docker-rootless-install.sh && \
#     sh docker-rootless-install.sh

# # Install docker -- version 1 download packages with apt
# RUN apt-get install -y \
#     apt-transport-https \
#     ca-certificates \
#     curl \
#     gnupg-agent \
#     software-properties-common
# RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
# RUN apt-key fingerprint 0EBFCD88
# RUN add-apt-repository \
#    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
#    $(lsb_release -cs) \
#    stable"
# RUN apt-get update -y
# RUN apt-get install -y docker-ce docker-ce-cli containerd.io

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
