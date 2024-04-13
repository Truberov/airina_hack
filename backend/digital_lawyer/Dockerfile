FROM python:3.10.8-slim
ENV PYTHONUNBUFFERED 1
ENV TZ 'Europe/Moscow'

RUN mkdir /code

RUN apt-get update && apt-get install -y git gcc libpq-dev postgresql-client \
    libjpeg-dev zlib1g-dev libwebp-dev gettext libwebp-dev

WORKDIR /code

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./digital_lawyer ./
EXPOSE 8000