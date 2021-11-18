FROM python:3.8
RUN mkdir /devstorage
RUN mkdir /web_django
WORKDIR /web_django
COPY requirements.txt /web_django/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt install -y nfs-common && mkdir /reports
ADD . /web_django
#CMD sudo mount -t nfs 200.200.200.234:/deploy_storage /devstorage