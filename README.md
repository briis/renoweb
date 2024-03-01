# // renoweb

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/briis/renoweb?include_prereleases&style=flat-square)

The renoweb integration adds support for retreiving Garbage Collection data from Municipalities around Denmark. The integration uses the same lookup API's as the Municipalities do, so if your Municipality uses RenoWeb as their data API, there is very good chance that this integration will work for you.

There is currently support for the following device types within Home Assistant:

* Calendar
* Sensor

The *state* of the sensor, will be number of days until next pick-up, and the next pickup dates will be shown in a local calendar

## MUNICIPALTIES NOT SUPPORTED
Unfortunately not all Municipalities use the API I use here, and therefore they are NOT supported, and CANNOT be added to the list.

As of writing this, I have found the following Municipalities to NOT work:
* Fåborg-Midtfyn
* København
* Århus


## CREDITS

A big thank you to @thomaspalmdk for finding the new API, and help test this new version.

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
calendar.py
config_flow.py
const.py
manifest.json
sensor.py
translation (Directory with all files)
```

## PRE-WORK

This integration uses the `entity_picture` attribute, which means you can get nice looking Pictograms instead of Icons on your dashboard. If you want to use this feature, do the following:
* download this [zip file](https://github.com/briis/renoweb/blob/main/images/renoweb.zip) and unzip the content. You should see a folder called `renoweb` with a bunch of `.svg` in it.
* Open a file share to the `config` share on your Home Assistant entity, and go to the `www` directory. If this directory does not exist, just create it.
* Now copy the folder `renoweb` from the Zip file to the `www` directory and that is it. This is where this integration will look for the Entity Pictures.

## CONFIGURATION

In order to add this Integration to Home Assistant, go to *Settings* and *Integrations*. If you just installed RenoWeb, do a Hard Refresh in your browser, while on this page, to ensure the Integration shows up.

Now click the **+** button in the lower right corner, and then search for *Renoweb*. That should bring up the below screen:

![](https://github.com/briis/renoweb/blob/main/config_flow.png)

Now fill out the form and click the *SEND* button. The Integration should now find all data for your address and add the available sensors to Home Assistant.

**Please note** that under Municipality you can either type the name of the Municipality or if you allready have the ID number, you can type in this instead of the name.

## SUPPORTED MUNICIPALITIES
It is hard to tell exactly what Municipalities are supported. When pulling them from the API, the below are the ones found, but reality has shown that more Munipalities use the same API. So try and type in your Municipality, and see if it works, even though it is not on the list below.

If you **can't get your municipality to work** with this integration, I encourage you to try another approach developed by @kentora called [RenoWeb Legacy](https://github.com/kentora/renoweb-legacy). This uses a different part of the RenoWeb API, and might work for some other Municipalities.

As of October 2020, this is the list of supported Municipalities:

```txt
MUNICIPALITY LIST
**************************
1: Aalborg - ID: 851
2: Allerød - ID: 201
3: BOFA TEST - ID: 400
4: Billund - ID: 530
5: Brøndby - ID: 153
6: Dragør - ID: 155
7: Egedal - ID: 240
8: Esbjerg - ID: 561
9: Fredensborg - ID: 210
10: Frederikssund - ID: 250
11: Gentofte - ID: 157
12: Gladsaxe - ID: 159
13: Glostrup - ID: 161
14: Greve - ID: 253
15: Halsnæs - ID: 260
16: Helsingør - ID: 217
17: Herlev - ID: 163
18: Hvidovre - ID: 167
19: Høje-Taastrup - ID: 169
20: Køge - ID: 259
21: Lejre - ID: 350
22: Lyngby-Taarbæk - ID: 173
23: Mariagerfjord - ID: 846
24: Ringkøbing-Skjern - ID: 760
25: Roskilde - ID: 265
26: Rudersdal - ID: 230
27: Rødovre Kommune - ID: 175
28: Samsø - ID: 741
29: Solrød - ID: 269
30: Svendborg - ID: 479
31: Tårnby - ID: 185
32: Vejen - ID: 575
````
