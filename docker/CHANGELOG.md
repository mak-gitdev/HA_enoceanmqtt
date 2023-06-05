## 0.1.26

### Changed
None

### Added
- Add virtual A5-10-06 (mak-gitdev/HA_enoceanmqtt#46)
- Add '%' as unit of measurement for A5-20-01 current value field (mak-gitdev/HA_enoceanmqtt#53)
- Update F6-02-[01-02] to send status bits

### Fixed
- Use latest enocean-mqtt version which fixes status bits setting (see mak-gitdev/HA_enoceanmqtt#65 and embyt/enocean-mqtt#41 for more details)
- From now, use mak-gitdev/enocean as Python EnOcean Library which fixes "list index out of range error" thanks to @kridgo patch (see kipe/enocean#134 and kipe/enocean#138 for more details).

### Removed
None

## 0.1.25

### Fixed
- Fix issue mak-gitdev/HA_enoceanmqtt#41

## 0.1.24

### Changed
- **Change devices and entities unique ids. This may lead to some devices loosing some configurations such as zones, etc.**
- Add better support for A5-13-01. ID1, ID2 and ID3 are now supported. ID4 to ID6 will follow in another release.
- Use device triggers for D2-03-0A instead of binary sensors.

## Added
- Add support for virtual devices. We can now declare more than one device sending broadcast data. Only F6-02-01 and F6-02-02 are available at the moment.
- Add packet receipt date to all devices so that it is possible to know the last time the device has been seen.
- Add support for:
  - D2-01-0A
  - D2-01-0D
  - D2-01-0E
  - A5-13-[01-06]
  - A5-10-03
  - A5-10-05
  - A5-10-06
  - A5-10-10
  - A5-10-12
  - A5-08-[01-03]
  - A5-14-01
  - A5-14-0A
  - A5-20-01 (no control yet, only status)
  - A5-20-04 (no control yet, only status)
  - Initial support for A5-38-08 command 1
- Add measurement control entities for D2-01-0B, D2-01-0C and D2-01-0E.

### Removed
- Remove some unused entities from D2-01-xx devices to comply with the EEP documentation.

### Fixed
- Fixed issue mak-gitdev/HA_enoceanmqtt#37

## 0.1.23

**Note**: Rename versions in changelog

### Changed
- Rename not rounded entities `xx_temperature` and `xx_humidity` from A5-04-XX devices to `t_raw` and
  `h_raw`. These new entities are also disable by default.

### Added
- Add support for:
  - A5-02-[01-0B]
  - A5-02-[10-1B]
  - A5-02-20
  - A5-02-30
  - A5-06-[01-02]
  - A5-07-[01-03]
  - A5-13-01
  - D2-03-0A

### Removed
- Remove °F entities from A5-04-XX devices as HA seems to convert automatically °C to °F and vice-versa

### Fixed
- Fix status entity for A5-04-XX devices.
