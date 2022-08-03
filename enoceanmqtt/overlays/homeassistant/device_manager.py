# Author: Marc Alexandre K. <marcalexandrek-developer@yahoo.fr>
"""this class is a device manager for the Home Assistant overlay of enoceanmqtt"""

import logging
import os
from tinydb import TinyDB, Query

class DeviceManager():

    db = None

    def __init__(self, config, sensors):
        db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'device_db.json')
        self.db = TinyDB(db_file)
        logging.info("Device database correctly read/created")

    def _db_search_device_by_address(self, address):
        '''Search device in the database using the device address'''
        dev = Query()
        return self.db.search(dev.address == address) != []

    def _db_search_device_by_name(self, name):
        '''Search device in the database using the device name'''
        dev = Query()
        return self.db.search(dev.name == name) != []

    def _db_get_device_by_address(self, address):
        '''Get device from the database using the device address'''
        dev = Query()
        return self.db.search(dev.address == address)

    def _db_get_device_by_name(self, name):
        '''Get device from the database using the device address'''
        dev = Query()
        return self.db.search(dev.name == name)

    def _db_add_device(self, sensor, system = None):
        '''Add new device to the database'''
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
        '''Remove device from the database'''
        if self._db_search_device_by_address(sensor['address']):
            dev = Query()
            self.db.remove(dev.address == sensor['address'])
            return True
        return False