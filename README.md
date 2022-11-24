# EnOcean to MQTT bridge for Home Assistant

The [mapping.yaml](https://github.com/mak-gitdev/HA_enoceanmqtt/blob/support-new-eeps/enoceanmqtt/overlays/homeassistant/mapping.yaml) file in this branch lists the EEP that will be supported in the next release.  
You can use this file to use new supported devices without waiting for the next release.

## Updating your mapping.yaml file

As I don't have access to all EnOcean devices, I organized this script so that end-users can do field tests when requesting a new device support or add new device support themselves.  
For that, it requires modifying the mapping.yaml file.

Here are the steps to follow:
- First stop the addon.
- Then copy the [mapping.yaml](https://github.com/mak-gitdev/HA_enoceanmqtt/blob/support-new-eeps/enoceanmqtt/overlays/homeassistant/mapping.yaml) file to your home assistant `/config/mapping.yaml`. Note that `/config/` is the directory where you have your Home Assistant `configuration.yaml` file.
- Then, if you are using the addon, you have a configuration entry named `mapping_file`. Set this entry to `/config/mapping.yaml` and save your configuration.
- Finally, add your device in your device file and restart the addon.

After that you should see entities corresponding to your device in HA.

## Supported Devices
A non-ticked box means that the device has not been tested.

 - [x] `D2-01-0B` 
 - [x] `D2-01-0C`
 - [ ] `D2-01-0F`
 - [x] `D2-01-12`
 - [x] `D2-05-00`
 - [x] `F6-02-01`
 - [x] `F6-02-02`
 - [x] `F6-05-02`
 - [x] `F6-10-00` (**new** - available with current release)
 - [x] `D5-00-01`
 - [ ] `A5-04-01` (**new** - available with current release)
 - [ ] `A5-04-02` (**new** - requires next release)
 - [ ] `A5-04-03` (**new** - available with current release)
 - [ ] `A5-04-04` (**new** - requires next release)
 - [x] `A5-12-00` (**new** - requires next release)
 - [x] `A5-12-01`
