FROM python:3-alpine

ARG BUILD_VERSION

# Create config volume
VOLUME /config

# Create Working Directory
WORKDIR /app

# Install enoceanmqtt and requirements
RUN apk add --no-cache git && \
    python3 -m pip install --upgrade pip && \
    pip3 install pyyaml && \
    pip3 install tinydb && \
    pip3 install git+https://github.com/mak-gitdev/enocean.git && \
    git clone https://github.com/embyt/enocean-mqtt.git && \
    cd enocean-mqtt && python3 setup.py develop && cd .. && \
    if [ -z "${BUILD_VERSION##*.*.*}" ]; then \
        echo "Building development version ${BUILD_VERSION%-*}" && \
        git clone -b develop --single-branch --depth 1 https://github.com/mak-gitdev/HA_enoceanmqtt.git ; \
    else \
        echo "Building Stable version ${BUILD_VERSION%-*}" && \
        git clone -b master --single-branch --depth 1 https://github.com/mak-gitdev/HA_enoceanmqtt.git ; \
    fi; \
    cp -rf HA_enoceanmqtt/enoceanmqtt enocean-mqtt && \
    rm -rf HA_enoceanmqtt

# Set entrypoint
ENTRYPOINT [ "python", "/usr/local/bin/enoceanmqtt", "/config/enoceanmqtt.conf" ]
