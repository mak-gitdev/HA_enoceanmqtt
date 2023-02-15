# EnOcean to MQTT bridge for Home Assistant

This branch is used to interact with end-users requesting new device support.  

## Updating your mapping.yaml file

As I don't have access to all EnOcean devices, I organized HA_enoceanmqtt so that end-users can do field tests when requesting a new device support or add new device support themselves.  
For that, it requires modifying the mapping.yaml file and maybe also the EEP.xml file used by the EnOcean library.

Here are the steps to follow:
1. First stop the addon.
1. Then copy the [mapping.yaml](https://github.com/mak-gitdev/HA_enoceanmqtt/blob/support-new-eeps/enoceanmqtt/overlays/homeassistant/mapping.yaml) file to your home assistant `/config/<directory_you_want>/mapping.yaml`. Note that `/config/` is the directory where you have your Home Assistant `configuration.yaml` file.
1. Then, if you are using the addon, you have a configuration entry named `mapping_file`. Set this entry to `/config/<directory_you_want>/mapping.yaml`, which is the location where you saved the mapping.yaml file and save your configuration.
1. Similarly, copy the [EEP.xml](https://github.com/mak-gitdev/HA_enoceanmqtt/blob/support-new-eeps/enocean/protocol/EEP.xml) file to your home assistant `/config/<directory_you_want>/mapping.yaml`. Note that `/config/` is the directory where you have your Home Assistant `configuration.yaml` file.
1. Again, if you are using the addon, you have a configuration entry named `eep_file`. Set this entry to `/config/<directory_you_want>/EEP.xml`, which is the location where you saved the EEP.xml file and save your configuration.
1. Finally, add your device in your device file and restart the addon.

After that you should see entities corresponding to your device in HA.  

**Do not forget to undo steps 3 and 5 once your device is supported in the next release.**
