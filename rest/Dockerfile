FROM alpine:latest

RUN apk add --no-cache -q -f git python3 python3-dev gcc
RUN python3 -m ensurepip
RUN python3 -m pip install --upgrade pip

RUN apk add --no-cache -f  musl-dev linux-headers
COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN apk add --no-cache bash

COPY . .



RUN chmod 777 ./start.sh ./wait-for-it.sh

ENTRYPOINT "./start.sh"