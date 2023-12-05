#!/usr/bin/env python3
# Copyright (c) 2020 embyt GmbH. See LICENSE for further details.
# Author: Roman Morawek <roman.morawek@embyt.com>
"""this is the main entry point, which sets up the Communicator class"""
import logging
import sys
import os
import traceback
import copy
import argparse
from configparser import ConfigParser

from enoceanmqtt.communicator import Communicator

conf = {
    'debug': False,
    'config': ['/etc/enoceanmqtt.conf'],
    'logfile': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enoceanmqtt.log')
}


def parse_args():
    """ Parse command line arguments. """
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('--debug', help='enable console debugging', action='store_true')
    parser.add_argument('--logfile', help='set log file location')
    parser.add_argument('config', help='specify config file[s]', nargs='*')
    # parser.add_argument('--version', help='show application version',
    #     action='version', version='%(prog)s ' + VERSION)
    args = vars(parser.parse_args())
    # logging.info('Read arguments: ' + str(args))
    return args


def load_config_file(config_files):
    """load sensor and general configuration from given config files"""
    # extract sensor configuration
    sensors = []
    global_config = {}

    for conf_file in config_files:
        config_parser = ConfigParser(inline_comment_prefixes=('#', ';'), interpolation=None)
        if not os.path.isfile(conf_file):
            logging.warning("Config file %s does not exist, skipping", conf_file)
            continue
        logging.info("Loading config file %s", conf_file)
        if not config_parser.read(conf_file):
            logging.error("Cannot read config file: %s", conf_file)
            sys.exit(1)

        for section in config_parser.sections():
            if section == 'CONFIG':
                # general configuration is part of CONFIG section
                for key in config_parser[section]:
                    global_config[key] = config_parser[section][key]
            else:
                mqtt_prefix = config_parser['CONFIG']['mqtt_prefix'] \
                    if 'mqtt_prefix' in config_parser['CONFIG'] else "enocean/"
                new_sens = {'name': mqtt_prefix + section}
                for key in config_parser[section]:
                    try:
                        if key in ('command', 'channel', 'publish_json', 'default_data', 'model'):
                            new_sens[key] = config_parser[section][key]
                        else:
                            new_sens[key] = int(config_parser[section][key], 0)
                    except KeyError:
                        new_sens[key] = None
                sensors.append(new_sens)
                logging.debug("Created sensor: %s", new_sens)

    logging_global_config = copy.deepcopy(global_config)
    if "mqtt_pwd" in logging_global_config:
        logging_global_config["mqtt_pwd"] = "*****"
    logging.debug("Global config: %s", logging_global_config)

    return sensors, global_config


def setup_logging(log_filename='', log_level=logging.INFO):
    """initialize python logging infrastructure"""
    # create formatter
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    # set root logger to lowest log level
    logging.getLogger().setLevel(log_level)

    # create console and log file handlers and the formatter to the handlers
    log_console = logging.StreamHandler(sys.stdout)
    log_console.setFormatter(log_formatter)
    log_console.setLevel(log_level)
    logging.getLogger().addHandler(log_console)
    if log_filename:
        log_file = logging.FileHandler(log_filename)
        log_file.setLevel(log_level)
        log_file.setFormatter(log_formatter)
        logging.getLogger().addHandler(log_file)
        logging.info("Logging to file: %s", log_filename)


def main():
    """entry point if called as an executable"""
    # logging.getLogger().setLevel(logging.DEBUG)
    # Parse command line arguments
    conf.update(parse_args())

    # setup logger
    setup_logging(conf['logfile'], logging.DEBUG if conf['debug'] else logging.INFO)

    # load config file
    sensors, global_config = load_config_file(conf['config'])
    conf.update(global_config)

    # Select the overlay
    if str(global_config.get('overlay')).lower() == "ha":
        try:
            from enoceanmqtt.overlays.homeassistant.ha_communicator import HACommunicator
        except ImportError:
            logging.error("Unable to import Home Assistant overlay")
            return
        logging.info("Selected overlay : Home Assistant")
        com = HACommunicator(conf, sensors)
    else:
        logging.info("Selected overlay : None")
        com = Communicator(conf, sensors)

    # start working
    try:
        com.run()

    # catch all possible exceptions
    except:     # pylint: disable=broad-except,bare-except
        logging.error(traceback.format_exc())


# check for execution
if __name__ == "__main__":
    main()
