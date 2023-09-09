FROM python:3.9-slim
LABEL author="Kostya Kamanin" maintainer="Shishka"


WORKDIR /usr/src/app

COPY ../../../Downloads/shisha/shisha/backend .

RUN pip install -r reqs.txt