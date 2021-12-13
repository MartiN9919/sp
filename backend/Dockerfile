FROM python:3.8
ENV MODE='deploy'
RUN mkdir /devstorage
RUN mkdir /log
RUN mkdir /web_django
WORKDIR /web_django
COPY requirements.txt /web_django/
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install gunicorn
RUN export DEBIAN_FRONTEND=noninteractive && apt update && mkdir /reports
ADD . /web_django
CMD gunicorn --env DJANGO_SETTINGS_MODULE=core.deploy_settings core.wsgi:application -b :8000