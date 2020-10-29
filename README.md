# // renoweb

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/briis/renoweb?include_prereleases&style=flat-square)

The renoweb integration adds support for collecting Garbage Collection data from RenoWeb. This is a data provider for several Municipalities in Denmark.

There is currently support for the following device types within Home Assistant:

* Sensor

## Installation

### HACS Installation

This Integration is not part of the default HACS store, but you can add it as a Custom repository in HACS by doing the following:

1. Go to HACS in your HA installation, and click on *Integrations*
2. Click the three vertical dots in the upper right corner, and select *Custom repositories*
3. Add `https://github.com/briis/renoweb` and select *Integration* as Category, and then click *Add*

You should now be able to find this Integration in HACS. (Most times you need to do a Hard Refresh of the browser before it shows up)

### Manual Installation

To add *renowweb* to your installation, create this folder structure in your /config directory:

`custom_components/renoweb`.
Then, drop the following files into that folder:

```yaml
__init__.py
manifest.json
sensor.py
entity.py
config_flow.py
const.py
string.json
translation (Directory with all files)
```

## Credits

This module is solely based on the work done by **@esbenr** and **@AngelFreak**, who did all the work in sniffing out the API and Keys.
