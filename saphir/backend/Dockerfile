FROM python:3.8
RUN mkdir /web_django
WORKDIR /web_django
COPY requirements.txt /web_django/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN apt install nfs-common && mkdir /reports
RUN sudo mount -t nfs 200.200.200.234:/reports /reports
ADD . /web_django