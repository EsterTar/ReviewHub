# Используйте официальный образ Python 3.11
FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir \
     && ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime

COPY . /app

WORKDIR /app/src
