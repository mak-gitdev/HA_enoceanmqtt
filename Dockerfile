FROM python:3-alpine

VOLUME /config

COPY . /
RUN python setup.py develop

WORKDIR /
ENTRYPOINT ["python", "/usr/local/bin/enoceanmqtt", "/enoceanmqtt-default.conf", "/config/enoceanmqtt.conf"]
