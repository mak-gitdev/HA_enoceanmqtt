# Author: Marc Alexandre K. <marcalexandrek-developer@yahoo.fr>
"""this class is a Home Assistant overlay for enoceanmqtt"""

import logging
import copy
import os
import time
import json
import yaml

import enocean.utils
from enoceanmqtt.communicator import Communicator

from enoceanmqtt.overlays.homeassistant.device_manager import DeviceManager

class HACommunicator(Communicator):
    '''Home Assistant-oriented Communicator subclass for enoceanmqtt'''
    _mqtt_discovery_prefix = None
    _devmgr = None
    _first_mqtt_connect = True
    _system_status_topic = {}

    def __init__(self, config, sensors):
        # Read mapping file
        mapping_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mapping.yaml')
        with open(mapping_file, 'r', encoding="utf-8") as file:
            self._ha_mapping = yaml.safe_load(file)
        logging.info("HA Mapping file correctly read")

        # Overwrite some of the user-defined device configuration
        # to comply with the overlay requirements
        for cur_sensor in sensors:
            if str(cur_sensor.get('ignore')) not in ("True", "true", "1"):
                # Retrieve EEP-related device configuration
                rorg = cur_sensor['rorg']
                func = cur_sensor['func']
                type_ = cur_sensor['type']
                devcfg = {}
                try:
                    devcfg = self._ha_mapping[rorg][func][type_]['device_config']
                except KeyError:
                    pass

                # Set EEP-related device configuration
                cur_sensor['command'] = devcfg.get('command')
                cur_sensor['channel'] = devcfg.get('channel')
                cur_sensor['log_learn'] = devcfg.get('log_learn')

                # Better to work with JSON in HA so force JSON usage
                # Also force publish_rssi and persistent
                cur_sensor['publish_json'] = "True"
                cur_sensor['publish_rssi'] = "True"
                cur_sensor['persistent'] = "True"

        # Create device manager
        self._devmgr = DeviceManager(config)

        # Retrieve MQTT discovery prefix from configuration and make sure there is a trailing '/'
        self._mqtt_discovery_prefix = config.get('mqtt_discovery_prefix', 'homeassistant/')
        if self._mqtt_discovery_prefix[-1] != '/':
            self._mqtt_discovery_prefix += '/'

        # Init
        super().__init__(config, sensors)

        # Disable Teach-in on startup
        self.enocean.teach_in = False
        logging.info("Auto Teach-in is %s", "enabled" if self.enocean.teach_in else "disabled")


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

            # MQTT operations at startup only
            if self._first_mqtt_connect:
                # Add LEARN button in HA
                self._mqtt_discovery_system('learn')

                # LEARN status
                self.mqtt.publish(self._system_status_topic['learn'],
                                  'ON' if self.enocean.teach_in else 'OFF',
                                  retain=True)

                # Get all device addresses in DB
                known_addresses = self._devmgr.db_list_from_fields('address')

                # This will discover new added sensors in HA while updating existing sensors
                # configuration when sensor mapping has changed
                for cur_sensor in self.sensors:
                    if str(cur_sensor.get('ignore')) not in ("True", "true", "1"):
                        # Get sensor from DB if it exists
                        sensor_db = self._devmgr.db_get_device_by_address(cur_sensor['address'])
                        # Sensor discovery/update
                        cfgtopics = sensor_db.get('cfgtopics', None) if sensor_db else None
                        self._mqtt_discovery_sensor(cur_sensor, cfgtopics)
                        # Remove device from the address list
                        try:
                            known_addresses.remove(cur_sensor['address'])
                        except ValueError:
                            pass

                # Delete devices that are no more listed in config file
                for address in known_addresses:
                    sensor_db = self._devmgr.db_get_device_by_address(address)
                    # Remove all device's entities
                    for cfgtopic in sensor_db['cfgtopics']:
                        self.mqtt.publish(f"{self._mqtt_discovery_prefix}{cfgtopic}",
                                           "", retain=True)
                    # Remove the device from the database
                    self._devmgr.db_remove_device_by_address(address)

                # First MQTT connection is done
                self._first_mqtt_connect = False
        else:
            logging.error("Error connecting to MQTT broker: %s",
                          self.CONNECTION_RETURN_CODE[return_code]
                          if return_code < len(self.CONNECTION_RETURN_CODE) else return_code)

    def _on_mqtt_message(self, _mqtt_client, _userdata, msg):
        '''the callback for when a PUBLISH message is received from the MQTT server.'''
        # Intercept system messages
        if '/__system' in msg.topic:
            self._handle_system_msg(msg)
        # Device messages
        else:
            super()._on_mqtt_message(_mqtt_client, _userdata, msg)


    #=============================================================================================
    # SYSTEM
    #=============================================================================================
    def _mqtt_discovery_system(self, attr):
        device_map = copy.deepcopy(self._ha_mapping['system'][attr])
        for entity in device_map:
            cfg = entity['config']
            # Create a unique ID for the entity based on the transmitter ID
            if self.enocean_sender is None:
                self.enocean_sender = self.enocean.base_id
            sender = enocean.utils.combine_hex(self.enocean_sender)
            uid = 'enoceanmqtt_'+attr+'_'+format(sender, '08X')
            cfg['unique_id'] = uid

            # The entity name to be displayed in HA
            cfg['name'] = entity['name']

            # Associate all entities to the device in HA
            cfg['device'] = {}
            cfg['device']['name'] = 'ENOCEANMQTT'
            cfg['device']['identifiers'] = format(sender, '08X')
            cfg['device']['model'] = 'Virtual'
            cfg['device']['manufacturer'] = 'https://github.com/mak-gitdev/HA_enoceanmqtt'

            # The configuration topic defined for MQTT Discovery
            cfgtopic = f"{self._mqtt_discovery_prefix}{entity['component']}/{uid}/config"

            # Append defined entity's topics to the device topic
            for key in cfg:
                if "topic" in key:
                    if cfg[key] not in ("", None):
                        cfg[key] = self.conf['mqtt_prefix']+'__system/'+cfg[key]
                    else:
                        cfg[key] = self.conf['mqtt_prefix']+'__system'

            # Publish the device configuration to MQTT for discovery
            self.mqtt.publish(cfgtopic, json.dumps(cfg), retain=True)
        # listen to HA learn requests
        self.mqtt.subscribe(self.conf['mqtt_prefix']+'__system/'+attr+'/req/#')
        self._system_status_topic[attr] = self.conf['mqtt_prefix']+'__system/'+attr

    def _mqtt_discovery_sensor(self, sensor, prev_sensor_cfgtopics=None):
        '''Publish MQTT discovery configuration to Home Assistant'''
        if prev_sensor_cfgtopics is None:
            prev_sensor_cfgtopics = []
        update = prev_sensor_cfgtopics != []
        rorg = sensor['rorg']
        func = sensor['func']
        type_ = sensor['type']
        eep_dash = f'{rorg:02X}'+'-'+f'{func:02X}'+'-'+f'{type_:02X}'

        # If the device is supported, retrieve the device mapping
        device_map = None
        try:
            device_map = copy.deepcopy(self._ha_mapping[rorg][func][type_]['entities'])
        except KeyError:
            pass

        if device_map is None:
            logging.warning('Device %s not supported yet. Only RSSI sensor will be available',
                            eep_dash)
            device_map = []

        # Add RSSI sensor in HA
        device_map += copy.deepcopy(self._ha_mapping['common']['rssi'])

        # Add Per device delete button in HA
        device_map += copy.deepcopy(self._ha_mapping['system']['delete'])

        eep = format((rorg<<16)+(func<<8)+type_, '06X')
        address = format(sensor['address'],'08X')
        device = "e2m_"+sensor['name'].replace(self.conf['mqtt_prefix'], "").replace("/", "_")
        sensor_cfgtopics = []

        # Loop over all the entities defined in the device
        for entity in device_map:
            # A name should be defined in mapping. If not, generate one.
            if str(entity.get('name')).lower() in ("none", ""):
                entity['name'] = str(int(time.time()))
            # Select the entity configuration
            cfg = entity['config']

            # Create a unique ID for the entity
            uid = "enocean_"+eep+"_"+address+"_"+entity['name']
            cfg['unique_id'] = uid

            # The entity name to be displayed in HA
            cfg['name'] = device+'_'+entity['name']

            # Associate all entities to the device in HA
            cfg['device'] = {}
            cfg['device']['name'] = device
            cfg['device']['identifiers'] = address
            cfg['device']['model'] = eep_dash+" @"+address
            cfg['device']['manufacturer'] = "EnOcean"

            # The configuration topic defined for MQTT Discovery
            cfgtopic = f"{entity['component']}/{uid}/config"

            # Remove the entity from the list of entities to be deleted during update
            if cfgtopic in prev_sensor_cfgtopics:
                prev_sensor_cfgtopics.remove(cfgtopic)

            # List of entities configuration topics for later component deletion/update
            sensor_cfgtopics.append(cfgtopic)

            # Append defined entity's topics to the device topic
            for key in cfg:
                if "topic" in key:
                    if cfg[key] not in ("", None):
                        cfg[key] = sensor['name']+"/"+cfg[key]
                    else:
                        cfg[key] = sensor['name']

            # Publish the device configuration to MQTT for discovery
            self.mqtt.publish(f"{self._mqtt_discovery_prefix}{cfgtopic}",
                              json.dumps(cfg), retain=True)

        # Delete to-be-deleted entities, if any
        for cfgtopic in prev_sensor_cfgtopics:
            self.mqtt.publish(f"{self._mqtt_discovery_prefix}{cfgtopic}", "", retain=True)

        # Subscribe to system message topic (per-device)
        self.mqtt.subscribe(sensor['name']+'/__system/#')

        # Add/update device to the database
        self._devmgr.db_upsert_device(sensor,  sensor_cfgtopics, 'cfgtopics')
        logging.info("Device %s (@: %s / EEP: %s) %s device database",
                     sensor['name'], address, eep_dash,
                     'updated on' if update else 'added to')

    def _handle_system_msg(self, msg):
        '''Handle system-related MQTT messages'''
        logging.debug("Received system message %s", msg)
        # Retrieve system request target
        [target_name, prop] = [msg.topic.split('/__system')[i] for i in (0,-1)]
        # Global system request
        if target_name == self.conf['mqtt_prefix'][:-1]:
            # Handle learn request
            if prop == "/learn/req":
                self.enocean.teach_in = msg.payload.decode('UTF-8') == 'ON'
                self.mqtt.publish(self._system_status_topic['learn'],
                                  'ON' if self.enocean.teach_in else 'OFF',
                                  retain=True)
        # Device system request
        else:
            sensor = self._devmgr.db_get_device_by_name(target_name)
            action = msg.payload.decode('UTF-8')
            logging.debug("Action %s received for sensor %s", action, str(sensor))
            if sensor not in ([], None):
                # Handle delete sensor request
                if action == "delete":
                    # Remove all sensor's entities
                    for cfgtopic in sensor['__system']:
                        self.mqtt.publish(f"{self._mqtt_discovery_prefix}{cfgtopic}",
                                           "", retain=True)
                    # Remove the sensor from the database
                    self._devmgr.db_remove_device_by_address(sensor['address'])


    #=============================================================================================
    # ENOCEAN TO MQTT
    #=============================================================================================
    def _publish_mqtt(self, sensor, mqtt_json):
        '''Publish decoded packet content to MQTT'''
        ## Present the device to HA if it is the first time it is seen
        #if not self._devmgr.db_search_device_by_address(sensor['address']):
            #self._mqtt_discovery_sensor(sensor)

        # Publish the packet
        super()._publish_mqtt(sensor, mqtt_json)
