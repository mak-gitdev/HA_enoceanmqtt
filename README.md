# Home Assistant Overlay for enoceanmqtt

This is a [Home Assistant](https://www.home-assistant.io/) overlay for [enoceanmqtt](https://github.com/embyt/enocean-mqtt).  
It allows to easily have access to EnOcean devices in Home Assistant through MQTT.  
It is based on MQTT discovery from the Home Assistant MQTT integration.  

<img src="https://raw.githubusercontent.com/mak-gitdev/HA_enoceanmqtt/develop/.github/images/diagram.svg" alt="Diagram" width="75%"/>
<br/><br/>

EnOceanMQTT is the core of HA_enoceanmqtt. It manages the EnOcean protocol through the USB300 dongle thanks to the [Python EnOcean library](https://github.com/kipe/enocean).  

The Python EnOcean library is based on an EEP.xml file which contains the definition of the supported EnOcean EEPs.  
As for EnOceanMQTT, it needs a configuration file in which are indicated among other things the MQTT parameters as well as the EnOcean devices to manage.  
The Home Assistant overlay is in charge of creating automatically and managing MQTT devices in Home Assistant. It maps an EnOcean device to one or more MQTT devices in HA thanks to a mapping file.  

# Standalone Installation

HA_enoceanmqtt can be installed as a standard python application on a Linux system.

<img src="https://raw.githubusercontent.com/mak-gitdev/HA_enoceanmqtt/develop/.github/images/install_supervised.svg" alt="Install Supervised" width="75%"/>
<br/><br/>

See [Standalone installation](https://github.com/mak-gitdev/HA_enoceanmqtt/wiki/Standalone-Installation) for more details.

# Docker Installation

HA_enoceanmqtt is also available as a docker image.  

<img src="https://raw.githubusercontent.com/mak-gitdev/HA_enoceanmqtt/develop/.github/images/install_docker.svg" alt="Install Docker" width="75%"/>
<br/><br/>

This installation will mainly suits users of Home Assistant container.  
See [Docker Installation](https://github.com/mak-gitdev/HA_enoceanmqtt/wiki/Docker-Installation) for more details.

# Home Assistant Addon Installation

HA_enoceanmqtt can also be installed as a Home Assistant addon.  

<img src="https://raw.githubusercontent.com/mak-gitdev/HA_enoceanmqtt/develop/.github/images/install_addon.svg" alt="Install Addon" width="75%"/>
<br/><br/>

This installation suits all Home Assistant installations with Supervisor.  
See [Home Assistant Addon Installation](https://github.com/mak-gitdev/HA_enoceanmqtt/wiki/Home-Assistant-Addon) for more details.

# Usage

Refer to [Usage](https://github.com/mak-gitdev/HA_enoceanmqtt/wiki/Usage) for more details.

# Supported Devices

Refer to [Supported devices](https://github.com/mak-gitdev/HA_enoceanmqtt/wiki/Supported-devices) for a list of supported devices.

For devices not yet supported, only the RSSI sensor is created in Home Assistant.  

**Note**: If your device is not supported yet, please feel free to ask me for adding your device through the discussion panel. Or feel free to add it to *__`mapping.yaml`__* and make a pull request (see [Contributing](https://github.com/mak-gitdev/HA_enoceanmqtt/wiki/Contributing) for more details).

# Additional Information

The [Wiki](https://github.com/mak-gitdev/HA_enoceanmqtt/wiki) page is filled with useful information.  
A [discussion](https://github.com/mak-gitdev/HA_enoceanmqtt/discussions) panel is also available. Do not hesitate to read it and use it.  
You can also take a closer look at the work in progress on this [page](https://github.com/users/mak-gitdev/projects/1).
