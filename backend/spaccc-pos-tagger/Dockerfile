# # https://docs.docker.com/compose/gettingstarted/

# # FROM python:3.7-alpine
# # FROM docker
# # FROM ubuntu:18.04
# FROM alpine

# # ---------------------------------
# # Install docker -- version 0 download packages with apk
# RUN apk add docker openrc
# RUN apk update
# RUN rc-update add docker boot
# # RUN service docker start
# # RUN service docker status

# # -----------------------------------------

# # # Install docker -- version 1 download packages with apt
# # RUN apt update
# # RUN apt install -y \
# #     apt-transport-https \
# #     ca-certificates \
# #     curl \
# #     gnupg-agent \
# #     software-properties-common
# # RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
# # RUN apt-key fingerprint 0EBFCD88
# # RUN add-apt-repository \
# #    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
# #    $(lsb_release -cs) \
# #    stable"
# # RUN apt update
# # RUN apt install -y docker-ce docker-ce-cli containerd.io


# # Manage Docker as a non-root user
# # https://docs.docker.com/install/linux/linux-postinstall/
# # RUN groupadd docker
# # RUN usermod -aG docker $USER
# # RUN newgrp docker

# WORKDIR /app
# # RUN apk add --no-cache gcc musl-dev linux-headers
# COPY requirements.txt requirements.txt
# RUN apk add python3 python-pip
# # RUN pip install -r requirements.txt
# RUN python3 -m pip install -r requirements.txt
# # RUN echo "alias python=python3" >> ~/.bashrc && /bin/bash -c "source ~/.bashrc"
# COPY . .
# # ENV FLASK_APP app.py
# # ENV FLASK_RUN_HOST 0.0.0.0
# CMD flask run
# # CMD ["/usr/bin/python3", "app.py"]


# -----------------------------------------------------------------------------

FROM python:3.7
# FROM ubuntu:18.04

# Install Singularity
# https://sylabs.io/guides/3.1/user-guide/installation.html

## Singularity dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libssl-dev \
#     uuid-dev \
#     libgpgme11-dev \
#     squashfs-tools \
#     libseccomp-dev \
#     wget \
#     pkg-config

# RUN export VERSION=3.0.3 && \
#     mkdir -p $GOPATH/src/github.com/sylabs && \
#     cd $GOPATH/src/github.com/sylabs && \
#     wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
#     tar -xzf singularity-${VERSION}.tar.gz && \
#     cd ./singularity && \
#     ./mconfig

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
# CMD /usr/bin/python3.7 -m app.py
