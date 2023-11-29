FROM python:3-alpine

ARG BUILD_VERSION

# Create config volume
VOLUME /config

# Create Working Directory
WORKDIR /app

# Install enoceanmqtt and requirements
RUN apk add --no-cache git
RUN python3 -m pip install --upgrade pip && \
    pip3 install pyyaml==6.0.1 && \
    pip3 install tinydb==4.7.1 && \
    pip3 install paho-mqtt==1.6.1 && \
    pip3 install git+https://github.com/mak-gitdev/enocean.git && \
    pip3 install git+https://github.com/embyt/enocean-mqtt.git

COPY HA_enoceanmqtt HA_enoceanmqtt/

# Set entrypoint
ENTRYPOINT [ "python", "-m", "HA_enoceanmqtt.main", "/config/enoceanmqtt.conf" ]
