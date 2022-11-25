#!/usr/bin/with-contenv bashio

bashio::log.green "Preparing to start..."

bashio::config.require 'device_file'

# Set files to be used
export CONFIG_FILE="/data/enoceanmqtt.conf"
export DB_FILE="/data/enoceanmqtt_db.json"
export DEVICE_FILE="$(bashio::config 'device_file')"
export LOG_FILE="$(bashio::config 'log_file')"
export MAPPING_FILE="$(bashio::config 'mapping_file')"
bashio::log.blue "Retrieved devices file: $DEVICE_FILE"

# Retrieve MQTT connection parameters
if bashio::config.is_empty 'mqtt_broker'; then
  if bashio::var.has_value "$(bashio::services 'mqtt')"; then
    export MQTT_HOST="$(bashio::services 'mqtt' 'host')"
    export MQTT_PORT="$(bashio::services 'mqtt' 'port')"
    export MQTT_USER="$(bashio::services 'mqtt' 'username')"
    export MQTT_PSWD="$(bashio::services 'mqtt' 'password')"
  fi
else
  export MQTT_HOST="$(bashio::config 'mqtt_broker.host')"
  export MQTT_PORT="$(bashio::config 'mqtt_broker.port')"
  export MQTT_USER="$(bashio::config 'mqtt_broker.user')"
  export MQTT_PSWD="$(bashio::config 'mqtt_broker.pwd')"
fi

# Check MQTT parameters
if [ -z "${MQTT_HOST}" ] || \
   [ -z "${MQTT_PORT}" ] || \
   [ -z "${MQTT_USER}" ] || \
   [ -z "${MQTT_PSWD}" ]; then
  bashio::log.blue "mqtt_host = $MQTT_HOST"
  bashio::log.blue "mqtt_port = $MQTT_PORT"
  bashio::log.blue "mqtt_user = $MQTT_USER"
  bashio::log.blue "mqtt_pwd  = $MQTT_PSWD"
  bashio::exit.nok "MQTT broker connection not fully configured"
fi

# Debug parameter
if bashio::var.true "$(bashio::config 'debug')"; then
  export DEBUG_FLAG="--debug"
else
  export DEBUG_FLAG=""
fi

# Create enoceanmqtt configuration file
echo "[CONFIG]"                                                           > $CONFIG_FILE
echo "enocean_port          = $(bashio::config 'enocean_port')"          >> $CONFIG_FILE
echo "log_packets           = $(bashio::config 'log_packets')"           >> $CONFIG_FILE
echo "overlay               = HA"                                        >> $CONFIG_FILE
echo "db_file               = $DB_FILE"                                  >> $CONFIG_FILE
echo "mapping_file          = $MAPPING_FILE"                             >> $CONFIG_FILE
echo "mqtt_discovery_prefix = $(bashio::config 'mqtt_discovery_prefix')" >> $CONFIG_FILE
echo "mqtt_host             = $MQTT_HOST"                                >> $CONFIG_FILE
echo "mqtt_port             = $MQTT_PORT"                                >> $CONFIG_FILE
echo "mqtt_client_id        = $(bashio::config 'mqtt_client_id')"        >> $CONFIG_FILE
echo "mqtt_keepalive        = $(bashio::config 'mqtt_keepalive')"        >> $CONFIG_FILE
echo "mqtt_prefix           = $(bashio::config 'mqtt_prefix')"           >> $CONFIG_FILE
echo "mqtt_user             = $MQTT_USER"                                >> $CONFIG_FILE
echo "mqtt_pwd              = $MQTT_PSWD"                                >> $CONFIG_FILE
echo "mqtt_debug            = $(bashio::config 'debug')"                 >> $CONFIG_FILE
echo ""                                                                  >> $CONFIG_FILE
cat $DEVICE_FILE                                                         >> $CONFIG_FILE

# Delete previous session log
rm -f $LOG_FILE

bashio::log.green "Starting EnOceanMQTT..."
enoceanmqtt $DEBUG_FLAG --logfile $LOG_FILE $CONFIG_FILE
