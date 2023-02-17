# Author: Marc Alexandre K. <marcalexandrek-developer@yahoo.fr>
"""this class is a device manager for the Home Assistant overlay of enoceanmqtt"""

import logging
import os
from tinydb import TinyDB, Query

class DeviceManager():
    '''Device Manager class, providing database methods'''

    _db = None

    def __init__(self, config):
        db_file = config.get('db_file')
        if not db_file:
            db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'device_db.json')
        self._db = TinyDB(db_file, indent=4)
        self.db_add_uid()
        logging.info("Device database %s correctly read/created", db_file)

    def db_add_uid(self):
        '''Update old databases without UID'''
        for device in self.db_get_devices():
            if not device.get('uid'):
                eep = format((device['rorg']<<16)+(device['func']<<8)+device['type'], '06X')
                device['uid'] = eep+"_"+format(device['address'],'08X')+"_NONE"
                dev = Query()
                self._db.update(device, dev.address == device['address'])

    def db_search_device_by_address(self, address):
        '''Search device in the database using the device address'''
        dev = Query()
        return self._db.contains(dev.address == address)

    def db_search_device_by_name(self, name):
        '''Search device in the database using the device name'''
        dev = Query()
        return self._db.contains(dev.name == name)

    def db_search_device_by_field(self, field_name, field):
        '''Search device in the database using a device field'''
        dev = Query()
        if type(field) is list:
            return self._db.contains(dev[field_name].all([field]))
        return self._db.contains(dev[field_name] == field)

    def db_get_device_by_address(self, address):
        '''Get device from the database using the device address'''
        dev = Query()
        return self._db.get(dev.address == address)

    def db_get_device_by_name(self, name):
        '''Get device from the database using the device name'''
        dev = Query()
        return self._db.get(dev.name == name)

    def db_get_device_by_field(self, field_name, field):
        '''Get device from the database using a device field'''
        dev = Query()
        if type(field) is list:
            return self._db.get(dev[field_name].all([field]))
        return self._db.get(dev[field_name] == field)

    def db_get_devices(self):
        '''Get all devices from the database'''
        return self._db.all()

    def db_list_from_fields(self, field):
        '''Get a list of field values for all devices in the database'''
        field_list = []
        for sensor in self._db.all():
            field_list.append(sensor[field])
        return field_list

    def db_add_device(self, sensor, uid, attr_name = None, attr = None):
        '''Add new device to the database'''
        if not self.db_search_device_by_address(sensor['address']):
            sensor_db = {}
            sensor_db['uid']     = uid
            sensor_db['address'] = sensor['address']
            sensor_db['name']    = sensor['name']
            sensor_db['rorg']    = sensor['rorg']
            sensor_db['func']    = sensor['func']
            sensor_db['type']    = sensor['type']
            if attr is not None:
                sensor_db[attr_name]= attr
            self._db.insert(sensor_db)
            return True
        return False

    def db_update_device(self, sensor, uid, attr_name = None, attr = None):
        '''Update device on the database'''
        if self.db_search_device_by_field('uid', sensor['uid']):
            sensor_db = {}
            sensor_db['name'] = sensor['name']
            if attr is not None:
                sensor_db[attr_name] = attr
            dev = Query()
            self._db.update(sensor_db, dev.uid == uid)
            return True
        return False

    def db_upsert_device(self, sensor, uid, attr_name = None, attr = None):
        '''Update or add device to the database'''
        sensor_db = {}
        sensor_db['uid']     = uid
        sensor_db['address'] = sensor['address']
        sensor_db['name']    = sensor['name']
        sensor_db['rorg']    = sensor['rorg']
        sensor_db['func']    = sensor['func']
        sensor_db['type']    = sensor['type']
        if attr is not None:
            sensor_db[attr_name] = attr
        dev = Query()
        self._db.upsert(sensor_db, dev.uid == uid)

    def db_remove_device_by_address(self, address):
        '''Remove device from the database using device address'''
        if self.db_search_device_by_address(address):
            dev = Query()
            self._db.remove(dev.address == address)
            return True
        return False

    def db_remove_device_by_field(self, field_name, field):
        '''Remove device from the database using a device field'''
        sensor = self.db_get_device_by_field(field_name, field)
        if sensor:
            dev = Query()
            # Remove the sensor from the database
            if type(field) is list:
                ids = self._db.remove(dev[field_name].all([field]))
            else:
                ids = self._db.remove(dev[field_name] == field)

            if ids:
                logging.debug("Delete request for sensor %s (UID %s): DONE",sensor['name'],sensor['uid'])
                return True
            else:
                logging.debug("Delete request for sensor %s (UID %s): ERROR",sensor['name'],sensor['uid'])
                return False
        return False
