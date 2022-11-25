ARG BUILD_FROM
FROM $BUILD_FROM

ARG BUILD_VERSION

# Create Working Directory
WORKDIR /app

# Install enoceanmqtt and requirements
RUN apk add --no-cache python3 py3-pip git && \
    python3 -m pip install --upgrade pip && \
    pip3 install pyyaml && \
    pip3 install tinydb && \
    git clone https://github.com/embyt/enocean-mqtt.git && \
    cd enocean-mqtt && \
    python3 setup.py develop && \
    cd .. && \
    if [ "${BUILD_VERSION}" = "dev" ]; \
    then \
        echo "Installing development version" && \
        git clone -b develop --single-branch --depth 1 https://github.com/mak-gitdev/HA_enoceanmqtt.git && \
        cp -f HA_enoceanmqtt/addon-dev/run.sh /app ; \
    else \
        echo "Installing Stable version ${BUILD_VERSION%-*}" && \
        git clone -b master --single-branch --depth 1 https://github.com/mak-gitdev/HA_enoceanmqtt.git && \
        cp -f HA_enoceanmqtt/addon/run.sh /app ; \
    fi; \
    chmod a+x /app/run.sh && \
    cp -rf HA_enoceanmqtt/enoceanmqtt enocean-mqtt && \
    cp -rf HA_enoceanmqtt/enocean/protocol/EEP.xml \
        $(find / -path ./HA_enoceanmqtt -prune -o -name "EEP.xml" -print -quit 2>/dev/null) && \
    rm -rf HA_enoceanmqtt

CMD [ "/app/run.sh" ]
