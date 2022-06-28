FROM python:3.8
ENV MODE='deploy'
ENV TZ=Europe/Minsk
RUN mkdir /deploy_storage
RUN mkdir /log
RUN mkdir /web_django
WORKDIR /web_django
COPY requirements.txt /web_django/
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install gunicorn
RUN export DEBIAN_FRONTEND=noninteractive && apt update && mkdir /reports
ADD . /web_django
ARG SERVER_PORT="0.0.0.0:8000"
ENV PORT ${SERVER_PORT}
CMD gunicorn --env DJANGO_SETTINGS_MODULE=core.deploy_settings core.wsgi:application -b ${PORT}