# syntax=docker/dockerfile:1

FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./employee/requirements.txt /app/requirements.txt
RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# COPY . /app
# CMD [ "python","run.py" ]