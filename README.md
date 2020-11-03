# // renoweb

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/briis/renoweb?include_prereleases&style=flat-square)

The renoweb integration adds support for collecting Garbage Collection data from RenoWeb. This is a data provider for several Municipalities in Denmark.

There is currently support for the following device types within Home Assistant:

* Sensor

The *state* of the sensor, will be number of days until next pick-up

## CREDITS

This module is solely based on the work done by **Jacob Henriksen**, **@esbenr** and **@AngelFreak**, who did all the work in sniffing out the API and Keys. I took their work and just converted it in to a Home Assistant Integration.

## INSTALLATION

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

## CONFIGURATION



## SUPPORTED MUNICIPALITIES

As of October 2020, this is the list of supported Municipalities:

```txt
MUNICIPALITY LIST
**************************
Allerød - ID: 201
Brøndby - ID: 153
Dragør - ID: 155
Egedal - ID: 240
Esbjerg - ID: 561
Fredensborg - ID: 210
Frederikssund - ID: 250
Gentofte - ID: 157
Gladsaxe - ID: 159
Glostrup - ID: 161
Greve - ID: 253
Helsingør - ID: 217
Herlev - ID: 163
Hillerød - ID: 219
Hvidovre - ID: 167
Høje-Taastrup - ID: 169
Kerteminde - ID: 440 (Need to use the ID when adding)
Køge - ID: 259
Lejre - ID: 350
Rebild - ID: 840
Ringkøbing-Skjern - ID: 760
Roskilde - ID: 265
Rudersdal - ID: 230
Solrød - ID: 269
Stevns - ID: 336
Svendborg - ID: 479
Tårnby - ID: 185
Vejen - ID: 575
Aalborg - ID: 851
````
