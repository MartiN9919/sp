FROM python:3.8
RUN mkdir /devstorage
RUN mkdir /log
RUN mkdir /web_django
WORKDIR /web_django
COPY requirements.txt /web_django/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt install -y nfs-common && mkdir /reports
ADD . /web_django
#sudo docker run --network host --name saphir_2.0 -v /devstorage:/devstorage saphir2.0 python manage.py runserver 0.0.0.0:80