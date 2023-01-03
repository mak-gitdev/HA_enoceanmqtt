# EnOcean to MQTT bridge for Home Assistant

This branch is used to interact with end-users requesting new device support.  

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
An unchecked box means that the device has not been tested.

<details><summary>A5</summary><blockquote>
  <details><summary>02</summary><blockquote>
    <ul><li>[ ] A5-02-01</li></ul>
    <ul><li>[ ] A5-02-02</li></ul>
    <ul><li>[ ] A5-02-03</li></ul>
    <ul><li>[ ] A5-02-04</li></ul>
    <ul><li>[ ] A5-02-05</li></ul>
    <ul><li>[ ] A5-02-06</li></ul>
    <ul><li>[ ] A5-02-07</li></ul>
    <ul><li>[ ] A5-02-08</li></ul>
    <ul><li>[ ] A5-02-09</li></ul>
    <ul><li>[ ] A5-02-0A</li></ul>
    <ul><li>[ ] A5-02-0B</li></ul>
    <ul><li>[ ] A5-02-10</li></ul>
    <ul><li>[ ] A5-02-11</li></ul>
    <ul><li>[ ] A5-02-12</li></ul>
    <ul><li>[ ] A5-02-13</li></ul>
    <ul><li>[ ] A5-02-14</li></ul>
    <ul><li>[ ] A5-02-15</li></ul>
    <ul><li>[ ] A5-02-16</li></ul>
    <ul><li>[ ] A5-02-17</li></ul>
    <ul><li>[ ] A5-02-18</li></ul>
    <ul><li>[ ] A5-02-19</li></ul>
    <ul><li>[ ] A5-02-1A</li></ul>
    <ul><li>[ ] A5-02-1B</li></ul>
    <ul><li>[ ] A5-02-20</li></ul>
    <ul><li>[ ] A5-02-30</li></ul>
  </blockquote></details>
  <details><summary>04</summary><blockquote>
    <ul><li>[ ] A5-04-01</li></ul>
    <ul><li>[x] A5-04-02</li></ul>
    <ul><li>[ ] A5-04-03</li></ul>
    <ul><li>[ ] A5-04-04</li></ul>
  </blockquote></details>
  <details><summary>06</summary><blockquote>
    <ul><li>[ ] A5-06-01</li></ul>
    <ul><li>[ ] A5-06-02</li></ul>
  </blockquote></details>
  <details><summary>07</summary><blockquote>
    <ul><li>[ ] A5-07-01</li></ul>
    <ul><li>[ ] A5-07-02</li></ul>
    <ul><li>[ ] A5-07-03</li></ul>
  </blockquote></details>
  <details><summary>12</summary><blockquote>
    <ul><li>[ ] A5-12-00</li></ul>
    <ul><li>[x] A5-12-01</li></ul>
  </blockquote></details>
  <details><summary>13</summary><blockquote>
    <ul><li>[ ] A5-13-01</li></ul>
  </blockquote></details>
  <details><summary>38</summary><blockquote>
    <ul><li>[ ] A5-38-08</li></ul>
  </blockquote></details>
</blockquote></details>

<details><summary>D2</summary><blockquote>
  <details><summary>01</summary><blockquote>
    <ul><li>[x] D2-01-0B</li></ul>
    <ul><li>[x] D2-01-0C</li></ul>
    <ul><li>[ ] D2-01-0F</li></ul>
    <ul><li>[x] D2-01-12</li></ul>
  </blockquote></details>
  <details><summary>03</summary><blockquote>
    <ul><li>[ ] D2-03-0A</li></ul>
  </blockquote></details>
  <details><summary>05</summary><blockquote>
    <ul><li>[x] D2-05-00</li></ul>
  </blockquote></details>
</blockquote></details>

<details><summary>D5</summary><blockquote>
  <details><summary>00</summary><blockquote>
    <ul><li>[x] D5-00-01</li></ul>
  </blockquote></details>
</blockquote></details>

<details><summary>F6</summary><blockquote>
  <details><summary>02</summary><blockquote>
    <ul><li>[x] F6-02-01</li></ul>
    <ul><li>[x] F6-02-02</li></ul>
  </blockquote></details>
  <details><summary>10</summary><blockquote>
    <ul><li>[x] F6-10-00</li></ul>
  </blockquote></details>
</blockquote></details>
