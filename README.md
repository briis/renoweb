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

In order to add this Integration to Home Assistant, go to *Settings* and *Integrations*. If you just installed RenoWeb, do a Hard Refresh in your browser, while on this page, to ensure the Integration shows up.

Now click the **+** button in the lower right corner, and then search for *Renoweb*. That should bring up the below screen:

![](https://github.com/briis/renoweb/blob/main/config_flow.png)

Now fill out the form and click the *SEND* button. The Integration should now find all data for your address and add the available sensors to Home Assistant.

**Please note** that under Municipality you can either type the name of the Municipality or if you allready have the ID number, you can type in this instead of the name.

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
