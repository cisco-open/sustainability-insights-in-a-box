# Configuring Device Inventory and Collection

Devices and collections are configured with a YAML file. This is mounted on Scheduler MS container.

## Configuration File Parameters

- loglevel:
  - console: Console log level, one of 'OFF', 'ERROR', 'INFO', 'DEBUG'
- sites:
  - site name: Unique site name
    - Latitude: Site latitude to fetch CO2 Intensity. Enter within quotes for YAML to interpret as string.
    - Longitude: Site longitude to fetch CO2 Intensity. Enter within quotes for YAML to interpret as string.
    - Timezone: Site timezone. Use the tz database naming convention
    - avg_co2_intensity: Site's CO2 Intensity override, where Electricity Map API is not available
- devices:
  - device name: Unique device name, must match the name configured on device 
  - site: Site name (from above) that the device belongs to
  - family: Device family either ASR1k or Cat9300
  - os_type: Device OS, only 'iosxe' supported in this version
  - os_version: Device OS version string '17.12.1'
  - connection: Connection type only 'ssh' supported in this version
  - address: Device IP address or hostname
  - port: Device SSH port to connect
  - ssh_options: SSH command line options used when connecting via ssh. Optional. Default value '-o KexAlgorithms=+diffie-hellman-group14-sha1 -o HostKeyAlgorithms=+ssh-rsa'
  - username: Device username
  - password: Device password in plain text, will be encyrpted on first run
  - timeout: Connection timeout in seconds
  - collection:
    - enabled: Flag to enable/disable collection, restart to take effect
    - interval: Collection interval in minutes

## Configuration Example
Below is an example configuration with two devices in two sites
```
loglevel:
  console: INFO
sites:
  branch:
    Latitude: '14.59'
    Longitude: '120.98'
    Timezone: Asia/Manila
    avg_co2_intensity: 570
  campus:
    Latitude: '37.375'
    Longitude: '-6.037'
    Timezone: Europe/Madrid
    avg_co2_intensity: 60
devices:
  ASR1k-A:
    site: branch
    family: ASR1k
    os_type: iosxe
    os_version: Unknown
    connection: ssh
    address: 10.10.0.1
    port: 22
    ssh_options: -o KexAlgorithms=+diffie-hellman-group14-sha1 -o HostKeyAlgorithms=+ssh-rsa
    username: admin
    password: password-encrypted-on-first-run
    timeout: 30
    collection:
      enabled: true
      interval: 10
  C9300-B:
    site: campus
    family: Cat9300
    os_type: iosxe
    os_version: Unknown
    connection: ssh
    address: 10.20.0.1
    port: 22
    ssh_options: -o KexAlgorithms=+diffie-hellman-group14-sha1 -o HostKeyAlgorithms=+ssh-rsa
    username: admin
    password: another-password-encrypted-on-first-run
    timeout: 30
    collection:
      enabled: true
      interval: 10
```

