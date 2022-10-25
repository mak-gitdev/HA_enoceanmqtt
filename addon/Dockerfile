ARG BUILD_FROM
FROM $BUILD_FROM

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
    curl -sL -o $(find / -name "EEP.xml" -print -quit 2>/dev/null) \
       https://raw.githubusercontent.com/mak-gitdev/enocean/master/enocean/protocol/EEP.xml && \
    git clone https://github.com/mak-gitdev/HA_enoceanmqtt.git && \
       cp -rf HA_enoceanmqtt/enoceanmqtt enocean-mqtt

# Copy data for add-on
# COPY enoceanmqtt enocean-mqtt/enoceanmqtt
COPY run.sh .
RUN chmod a+x run.sh

CMD [ "/app/run.sh" ]
