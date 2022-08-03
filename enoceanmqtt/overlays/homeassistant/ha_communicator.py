# Author: Marc Alexandre K. <marcalexandrek-developer@yahoo.fr>
"""this class is a Home Assistant overlay for enoceanmqtt"""

import logging
import copy
import os
import time
import yaml
import json

import enocean.utils
from enocean.protocol.constants import PACKET, RETURN_CODE, RORG
from enoceanmqtt.communicator import Communicator

from enoceanmqtt.overlays.homeassistant.device_manager import DeviceManager

class HACommunicator(Communicator):
    _mqtt_discovery_prefix = None
    _devmgr = None

    def __init__(self, config, sensors):
        # Better to work with JSON in HA so force JSON usage
        # Also force publish_rssi and persistent
        for cur_sensor in sensors:
            if str(cur_sensor.get('ignore')) not in ("True", "true", "1"):
                cur_sensor['publish_json'] = "True"
                cur_sensor['publish_rssi'] = "True"
                cur_sensor['persistent'] = "True"

        # Create device manager
        self._devmgr = DeviceManager(config, sensors)

        # Read mapping file
        mapping_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mapping.yaml')
        with open(mapping_file, 'r') as file:
            self.__ha_mapping = yaml.safe_load(file)
        logging.info("HA Mapping file correctly read")

        # Retrieve MQTT discovery prefix from configuration and make sure there is a trailing '/'
        self._mqtt_discovery_prefix = config.get('mqtt_discovery_prefix', 'enocean/discovery/')
        if self._mqtt_discovery_prefix[-1] != '/':
            self._mqtt_discovery_prefix += '/'

        # Init
        super().__init__(config, sensors)


    #=============================================================================================
    # MQTT CLIENT
    #=============================================================================================
    def _on_connect(self, mqtt_client, _userdata, _flags, return_code):
        '''callback for when the client receives a CONNACK response from the MQTT server.'''
        if return_code == 0:
            logging.info("Succesfully connected to MQTT broker.")
            # listen to enocean send requests
            for cur_sensor in self.sensors:
                mqtt_client.subscribe(cur_sensor['name']+'/req/#')

            # listen to HA system requests
            for cur_sensor in self._devmgr.db.all():
                mqtt_client.subscribe(cur_sensor['name']+'/__system/#')
        else:
            logging.error("Error connecting to MQTT broker: %s",
                          self.CONNECTION_RETURN_CODE[return_code]
                          if return_code < len(self.CONNECTION_RETURN_CODE) else return_code)

    def _on_mqtt_message(self, _mqtt_client, _userdata, msg):
        '''the callback for when a PUBLISH message is received from the MQTT server.'''
        if '/__system' in msg.topic:
            logging.debug("Received system message %s", msg)
            sensor_name = msg.topic.replace('/__system', '')
            sensor = self._devmgr._db_get_device_by_name(sensor_name)[0]
            logging.debug("Retrieved sensor %s", str(sensor))
            if sensor not in ([], None):
                if msg.payload.decode('UTF-8') == "delete":
                    for cfgtopic in sensor['__system']:
                        self.mqtt.publish(cfgtopic, "", retain=False)
                    self._devmgr._db_remove_device(sensor)
        else:
            super()._on_mqtt_message(_mqtt_client, _userdata, msg)


    #=============================================================================================
    # ENOCEAN TO MQTT
    #=============================================================================================
    def _mqtt_discovery(self, sensor):
        '''Publish MQTT discovery configuration to Home Assistant'''
        _rorg = sensor['rorg']
        _func = sensor['func']
        _type = sensor['type']
        _eep_dash = f'{_rorg:02X}'+'-'+f'{_func:02X}'+'-'+f'{_type:02X}'

        # If the device is supported, retrieve the device mapping
        device_map = None
        try:
            device_map = copy.deepcopy(self.__ha_mapping[_rorg][_func][_type])
        except:
          pass

        if device_map is None:
            logging.warning('Device %s not supported yet. Only RSSI sensor will be available', _eep_dash)
            device_map = []

        # Add RSSI sensor in HA
        device_map += copy.deepcopy(self.__ha_mapping['common']['rssi'])

        # Add Per device delete button in HA
        device_map += copy.deepcopy(self.__ha_mapping['system']['delete'])

        _eep = format((_rorg<<16)+(_func<<8)+_type, '06X')
        _address = format(sensor['address'],'08X')
        _device = "e2m_"+sensor['name'].replace(self.conf['mqtt_prefix'], "").replace("/", "_")
        _sys = []

        # Loop over all the entities defined in the device
        for entity in device_map:
            # A name should be defined in mapping. If not, generate one.
            if str(entity.get('name')).lower() in ("none", ""):
                entity['name'] = str(int(time.time()))
            # Select the correct configuration depending on the device's
            # EnOcean to MQTT message format
            if "system" in entity or str(sensor.get('publish_json')) not in ("True", "true", "1"):
                devcfg = entity['config']
            else:
                devcfg = entity['config_json']

            # Create a unique ID for the entity
            uid = "enocean_"+_eep+"_"+_address+"_"+entity['name']
            devcfg['unique_id'] = uid

            # The entity name to be displayed in HA
            devcfg['name'] = _device+'_'+entity['name']

            # Associate all entities to the device in HA
            devcfg['device'] = {}
            devcfg['device']['name'] = _device
            devcfg['device']['identifiers'] = _address
            devcfg['device']['model'] = _eep_dash+" @"+_address
            devcfg['device']['manufacturer'] = "EnOcean"

            # The configuration topic defined for MQTT Discovery
            cfgtopic = f"{self._mqtt_discovery_prefix}{entity['component']}/{uid}/config"
            # List of entities configuration topics for later component deletion
            _sys.append(cfgtopic)

            # Append defined entity's topics to the device topic
            for key in devcfg:
                if "topic" in key:
                    if devcfg[key] not in ("", None):
                        devcfg[key] = sensor['name']+"/"+devcfg[key]
                    else:
                        devcfg[key] = sensor['name']

            # Publish the device configuration to MQTT for discovery
            self.mqtt.publish(cfgtopic, json.dumps(devcfg), retain=True)

        # Subscribe to system message topic (per-device)
        self.mqtt.subscribe(sensor['name']+'/__system/#')

        # Add device to the database
        if self._devmgr._db_add_device(sensor, _sys):
            logging.info("Device %s (@: %s / EEP: %s) added to device database",
                         sensor['name'], _address, _eep_dash)

    def _publish_mqtt(self, sensor, channel_id, channel_value, mqtt_json):
        '''Publish decoded packet content to MQTT'''
        # Present the device to HA if it is the first time it is seen
        if not self._devmgr._db_search_device_by_address(sensor['address']):
            self._mqtt_discovery(sensor)

        # Publish the packet
        super()._publish_mqtt(sensor, channel_id, channel_value, mqtt_json)