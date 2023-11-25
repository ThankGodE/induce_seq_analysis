FROM debian:latest

LABEL image.author.name "ThankGod Ebenezer"
LABEL image.author.email "tee25@cam.ac.uk"

MAINTAINER "ThankGod Ebenezer"

WORKDIR /work_directory/

COPY induce_seq_analysis_python/requirements.txt /work_directory/

# Install base utilities
RUN apt update && \
    apt install -y build-essential  && \
    apt install -y wget && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# install python
RUN apt update && \
    apt install -y python3 && \
    apt install -y python3-pip && \
    apt install -y python3.11-venv

RUN python3 -m venv venv && \
   . venv/bin/activate && \
   pip install --upgrade pip && \
   pip install -r requirements.txt \








