FROM python:3.8.5-alpine3.12

RUN mkdir /usr/src/deviceprotect

WORKDIR /usr/src/deviceprotect

COPY . /usr/src/deviceprotect

RUN apk update \
  && apk add gcc musl-dev python3-dev libffi-dev openssl-dev \
  && pip install --upgrade pip \
  && pip install -r requirements/dev.txt \

