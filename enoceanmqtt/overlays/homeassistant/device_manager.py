# Author: Marc Alexandre K. <marcalexandrek-developer@yahoo.fr>
"""this class is a device manager for the Home Assistant overlay of enoceanmqtt"""

import logging
import os
from tinydb import TinyDB, Query

class DeviceManager():

    db = None
    #mqtt_discovery_prefix = None

    def __init__(self, config, sensors):
        #self.mqtt_discovery_prefix = config.get('mqtt_discovery_prefix', 'hassio/discovery')
        db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'device_db.json')
        self.db = TinyDB(db_file)
        logging.info("Device database correctly read/created")

        # Next step when we will try to remove enoceanmqtt.conf
        # Init DB with known sensors defined in enoceanmqtt.conf
        # for cur_sensor in sensors:
            # if str(cur_sensor.get('ignore')) not in ("True", "true", "1") and \
               # self._db_add_device(cur_sensor):
                # logging.info("Device %s (@: %s / EEP: %s-%s-%s) added to device database",
                             # cur_sensor['name'], f'{cur_sensor["address"]:08X}',
                             # f'{cur_sensor["rorg"]:02X}',
                             # f'{cur_sensor["func"]:02X}',
                             # f'{cur_sensor["type"]:02X}')

    def _db_search_device_by_address(self, address):
        dev = Query()
        return self.db.search(dev.address == address) != []

    def _db_search_device_by_name(self, name):
        dev = Query()
        return self.db.search(dev.name == name) != []

    def _db_get_device_by_address(self, address):
        dev = Query()
        return self.db.search(dev.address == address)

    def _db_get_device_by_name(self, name):
        dev = Query()
        return self.db.search(dev.name == name)

    def _db_add_device(self, sensor, system = None):
        if not self._db_search_device_by_address(sensor['address']):
            sensor_db = {}
            sensor_db['address'] = sensor['address']
            sensor_db['name']    = sensor['name']
            sensor_db['rorg']    = sensor['rorg']
            sensor_db['func']    = sensor['func']
            sensor_db['type']    = sensor['type']
            if system is not None:
                sensor_db['__system']= system
            self.db.insert(sensor_db)
            return True
        return False

    def _db_remove_device(self, sensor):
        if self._db_search_device_by_address(sensor['address']):
            dev = Query()
            self.db.remove(dev.address == sensor['address'])
            return True
        return False