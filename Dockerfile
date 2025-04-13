# Authors
# Jahziel Belmonte,
# Thomas viard

# This Dockerfile defines the container image for the application.
# It uses Python 3.13 as the base image and sets up the environment by:
# 1. Creating necessary directories
# 2. Installing Python dependencies from requirements.txt
# 3. Copying the application code into the container

FROM python:3.13

RUN mkdir /app /app/storage
RUN mkdir /app /app/media
WORKDIR /app

COPY requirements.txt  /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
