FROM python:3-alpine

ARG BUILD_VERSION

# Create config volume
VOLUME /config

# Create Working Directory
WORKDIR /app

# Install enoceanmqtt and requirements
RUN apk add --no-cache git && \
    python3 -m pip install --upgrade pip && \
    pip3 install pyyaml==6.0.1 && \
    pip3 install tinydb==4.7.1 && \
    pip3 install paho-mqtt==1.6.1 && \
    pip3 install git+https://github.com/mak-gitdev/enocean.git && \
    git clone -b master --single-branch --depth 1 https://github.com/embyt/enocean-mqtt.git && \
    cd enocean-mqtt && python3 setup.py develop && cd .. && \
    echo "Installing support-eltako branch" && \
    git clone -b support-eltako --single-branch --depth 1 https://github.com/mak-gitdev/HA_enoceanmqtt.git && \
    cp -rf HA_enoceanmqtt/enoceanmqtt enocean-mqtt && \
    rm -rf HA_enoceanmqtt

# Set entrypoint
ENTRYPOINT [ "python", "/usr/local/bin/enoceanmqtt", "/config/enoceanmqtt.conf" ]
