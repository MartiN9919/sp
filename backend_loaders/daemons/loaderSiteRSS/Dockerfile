FROM python:3.8 as build-python
WORKDIR /app/backend_loaders
RUN mkdir /devstorage /log /reports
COPY \
    ./../../lib ./lib && \
    ./../../daemons ./lib && \
    ./../../..backend_loaders/requirements.txt ./
RUN \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt update