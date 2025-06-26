
#clean environment for docker to run
FROM python:3.11-slim-bookworm

#Update the OS and install security patches
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

#Create the root directory similar to how app is already structured
WORKDIR /app

