import logging
import traceback

from enoceanmqtt.communicator import Communicator
from enoceanmqtt.enoceanmqtt import conf, parse_args, setup_logging, load_config_file


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
