# Home Assistant Overlay for enoceanmqtt

This is a [Home Assistant](https://www.home-assistant.io/) overlay for [enoceanmqtt](https://github.com/embyt/enocean-mqtt).  
It allows to easily have access to EnOcean devices in Home Assistant through MQTT.  
It is based on MQTT discovery from the Home Assistant MQTT integration.  

<img src="https://raw.githubusercontent.com/mak-gitdev/HA_enoceanmqtt/master/.github/images/diagram.svg" alt="Diagram" width="75%"/>
<br/><br/>

EnOceanMQTT is the core of HA_enoceanmqtt. It manages the EnOcean protocol through the USB300 dongle thanks to the [Python EnOcean library](https://github.com/kipe/enocean).  

The Python EnOcean library is based on an EEP.xml file which contains the definition of the supported EnOcean EEPs.  
As for EnOceanMQTT, it needs a configuration file in which are indicated among other things the MQTT parameters as well as the EnOcean devices to manage.  
The Home Assistant overlay is in charge of creating automatically and managing MQTT devices in Home Assistant. It maps an EnOcean device to one or more MQTT devices in HA thanks to a mapping file.  

## Standalone Installation

<img src="https://raw.githubusercontent.com/mak-gitdev/HA_enoceanmqtt/master/.github/images/install_supervised.svg" alt="Install Supervised" width="75%"/>
<br/><br/>

### Installation
For the moment, to install it, perform the following actions:

#### 1- Install enoceanmqtt
 - `pip install enocean-mqtt`

#### 2- Install pyyaml
 - `pip install pyyaml`

#### 3- Install TinyDB
 - `pip install tinydb`

#### 4- Install the Home Assistant overlay
 - Copy the *__`enoceanmqtt/`__* folder to enoceanmqtt

### Configuration
- adapt the `standalone/enoceanmqtt.conf.sample` file and put it to /etc/enoceanmqtt.conf:
   - Set the enocean interface port. Follow [these instructions](https://github.com/embyt/enocean-mqtt#define-persistant-device-name-for-enocean-interface) if you want to set a persistent device name for your enocean interface.
   - *`overlay = HA`* shall be added in the config section to indicate that the HA overlay is to be used.
   - *`mqtt_discovery_prefix = <prefix>`* shall also be added in the config section. where *`<prefix>`* is the MQTT prefix used for discovery. It defaults to `homeassistant` and can be configured in the Home Assistant MQTT integration as follow:
     ```yaml
     mqtt:
       discovery_prefix: <prefix>
     ```
     If you have other HA integrations using MQTT discovery (e.g. zigbee2mqtt, etc.), `<prefix>` should be set to `homeassistant` as it seems to be the one used in general.
   - Define the MQTT broker parameters
   - Define the `mqtt_prefix`. This is the prefix which will be used to interact with your EnOcean devices.  
     EnOceanMQTT will interact with EnOcean devices through the device root topic `<mqtt_prefix>/<device_name>`.
   - Define the devices to monitor. You only need to specify the device name, address, rorg, func and type.  
     **Tip**: Your device name can contain `/` e.g. `[lights/livingroom]`. This allows you to group your devices by type when exploring MQTT messages.
 - ensure that the MQTT broker is running
 - run `enoceanmqtt`


#### Setup as a daemon ####
Assuming you want this tool to run as a daemon, which gets automatically started by systemd:
 - Adapt and copy the `standalone/enoceanmqtt.service` to `/etc/systemd/system/`
 - `systemctl enable enoceanmqtt`
 - `systemctl start enoceanmqtt`

## Docker Installation
A docker image is not yet available but I am working on it.  

<img src="https://raw.githubusercontent.com/mak-gitdev/HA_enoceanmqtt/master/.github/images/install_docker.svg" alt="Install Docker" width="75%"/>
<br/><br/>

## Home Assistant Addon Installation
HA_enoceanmqtt can also be installed as a Home Assistant addon.  

<img src="https://raw.githubusercontent.com/mak-gitdev/HA_enoceanmqtt/master/.github/images/install_addon.svg" alt="Install Addon" width="75%"/>
<br/><br/>

### Installation
1. If you don't have a MQTT broker yet; in Home Assistant go to **Settings → Add-ons → Add-on store** and install the **Mosquitto broker** addon.
1. Go back to the **Add-on store**, click **⋮ → Repositories**, fill in</br>  `https://github.com/mak-gitdev/HA_enoceanmqtt` and click **Add → Close**.
1. Click on the addon and press **Install** and wait until the addon is installed.


### Configuration
1. Click on **Configuration**
    - Adapt the `addon/enoceanmqtt.devices.sample` and put it to your Home Assistant **/config** directory. You can use the Home Assistant **File Editor**.  
     **Tip**: Your device name can contain `/` e.g. `[lights/livingroom]`. This allows you to group your devices by type when exploring MQTT messages.
    - Indicate the location of your device file under the **device_file** entry.
    - Indicate your preferred location for the log file under the **log_file** entry. It shall be in your Home Assistant **/config** directory.
    - Select the serial interface of your EnOcean dongle in the list of detected serial ports. When using yaml configuration, the format is for example:
        ```yaml
        enocean_port: /dev/ttyUSB0
        ```
    - If you are **not** using the Mosquitto broker addon, fill in your MQTT details. Otherwise, leave empty the MQTT broker configuration. The format is for example:
        ```yaml
        host: localhost
        port: 1883
        user: my_user
        pwd: my_password
        ```
    - Indicate the `mqtt_discovery_prefix` under the **mqtt_discovery_prefix** entry. This is the MQTT prefix used for MQTT device discovery. It defaults to `homeassistant` and can be configured in the Home Assistant MQTT integration as follow:
        ```yaml
        mqtt:
          discovery_prefix: <prefix>
        ```
     If you have other HA integrations using MQTT discovery (e.g. zigbee2mqtt, etc.), **mqtt_discovery_prefix** should be set to `homeassistant/` as it seems to be the one used in general.
    - Indicate the `mqtt_prefix` under the **mqtt_prefix** entry. This is the prefix which will be used to interact with your EnOcean devices.  
      EnOceanMQTT will interact with EnOcean devices through the device root topic `<mqtt_prefix>/<device_name>`.
    - Turn on the **debug** switch if you want a very verbose log file.
    - Other settings can be kept to their default values.
    - Click **Save**
    - **Tip:** it is possible to refer to variables in the Home Assistant `secrets.yaml` file by using e.g. `pwd: !secret mqtt_pwd`
1. Start the addon by going to **Info** and click **Start**
1. Wait till HA_enoceanmqtt starts and press **Log** to verify HA_enoceanmqtt started correctly.

## Usage
### 1- Pairing your device
If pairing is needed, please follow the instruction of your device regarding pairing.  
Enoceanmqtt supports pairing through the Python EnOcean library.  
Once your device is in pairing mode, go to `Devices and Services` in HA, select the __`ENOCEANMQTT`__ device and turn on the __`LEARN`__ switch.  
The pairing response will be submitted automatically.  
Turn off the __`LEARN`__ switch once pairing is completed.  

### 2- Normal usage
Enoceanmqtt works as usual.  
The Home Assistant overlay is only in charge of creating automatically and managing MQTT devices in Home Assistant.  
At startup, all specified devices are created or updated in Home Assistant such that the user can directly interact with the device.  
Your devices will be available in Home Assistant under the MQTT integration's devices and entities.  

### 3- Delete your device from Home Assistant
If you want to delete your device from Home Assistant:
 - Remove your device from the enoceanmqtt device configuration file. You can at this stage, restart the addon and not follow the next steps. Follow the next steps if you don't want to restart the addon
 - Browse to the devices of MQTT integration
 - Click on your device
 - Click on the delete button in the configuration section

## Supported Devices
 - [x] `D2-01-0B` 
 - [x] `D2-01-0C`
 - [ ] `D2-01-0F` (not tested)
 - [x] `D2-01-12`
 - [x] `D2-05-00`
 - [x] `F6-02-01`
 - [x] `F6-02-02`
 - [x] `F6-05-02`
 - [x] `D5-00-01`
 - [ ] `A5-12-00` (not tested)
 - [x] `A5-12-01`

For devices not yet supported, only the RSSI sensor is created in Home Assistant.  

**Note**: If your device is not supported yet, please feel free to ask me for adding your device through the discussion panel. Or feel free to add it to *__`mapping.yaml`__* and make a pull request (see [adding new devices](https://github.com/mak-gitdev/HA_enoceanmqtt#adding-new-devices) for more details).

## Adding new devices
You can modify the *__`mapping.yaml`__* file to add new devices or new entities to already supported devices.  
Your changes will be taken into account after a restart.

A device is defined as, for example:
```yaml
0xD5:
   0x00:
      0x01:
         device_config:
            command: ""
            channel: ""
            log_learn: ""
         entities:
            - component: binary_sensor
              name: "contact"
              config:
                 state_topic: ""
                 value_template: "{{ value_json.CO }}"
                 payload_on: "0"
                 payload_off: "1"
```
<br/>

This indicates that the EnOcean device with EEP D5-00-01 will be mapped in Home Assistant to a single entity and that entity will be a binary sensor.

- `entities` is a list of the Home Assistant entities of the device.
  - `component` is the type of the entity
  - `name` defines the suffix that will be added after the device name to identify the entity.
    The entity name is of the form `e2m_<device_name>_<name>` where `<device_name>` is the name of the device set by the user in the device configuration file.
  - `config` defines the MQTT discovery configuration for the entity. Refer to the [MQTT Discovery documentation](https://www.home-assistant.io/docs/mqtt/discovery/) to properly set this field.
    You will also need the [EEP documentation](http://tools.enocean-alliance.org/EEPViewer) to correctly set topics and values.  
    As enoceanmqtt interacts with the device through the device root topic `<mqtt_prefix>/<device_name>`, MQTT entities topics are derived from this device root topic.  
    Hence, `state_topic = ""`  indicates that the `state_topic` to be used is the device root topic.  
    `state_topic = "<topic>"` would have indicated that the `state_topic` to be used is `<mqtt_prefix>/<device_name>/<topic>`.
- `device_config` indicates the enoceanmqtt parameters that should be used for this EEP. Refer to the [enoceanmqtt documentation](https://github.com/embyt/enocean-mqtt) to properly set this field.

Considering a user adds a D5-00-01 device in the device configuration file as follow:
```
[door_sensors/myD50001]
address = 0xBABECAFE
rorg = 0xD5
func = 0x00
type = 0x01
```

Then the user will have in Home Assistant, a device named `e2m_door_sensors_myD50001` with 3 new entities:
```
e2m_door_sensors_myD50001
   e2m_door_sensors_myD50001_contact
   e2m_door_sensors_myD50001_rssi (automatically generated entity for the device RSSI)
   e2m_door_sensors_myD50001_delete (automatically generated entity to delete the device from Home Assistant)
```

**Note**: Do not forget to make a pull request to integrate your changes.
