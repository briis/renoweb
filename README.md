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

## UPGRADING FROM VERSION 1.X

As of version 2.0, I am using a completely new API, and I have also used the opportunity to ensure this Integration delivers on the latest Home Assistant Requirements. All this means that there is NO directupgrade path from V1.x to this Version and all your sensors will get new names and new Unique ID's, which again means you will have to change automations, scripts and dashboard after installing this version.

If you never installed RenoWeb before go directly the Installation section.

Here is the suggested *"Upgrade"* Procedure:

#### Remove your current RenoWeb setup
1. Go to *Settings* | *Devices & Services
2. Click on *RenoWeb Garbage Collection*
3. Click on the 3 dots to the right of each address you installed, and click *Delete*
* **SKIP the next 3 steps, while the system is in Beta**
4. Now go to *HACS* and then click on *Integrations*
5. Find *RenoWeb Garbage Collection* and click on it.
6. You should now see the Integration description. In the upper right corder, click on the 3 dots, and then *Remove*
7. All is now removed, and it is recommended to restart Home Assistant

#### Add RenoWeb V2.0 to your system
* **This only applies while we are running the Beta, after that just you the normal Installation/Upgrade procedures**
* Go to *HACS* and then click on *Integrations*
* Find *RenoWeb Garbage Collection* and click on it.
* In the upper right corner, click on the 3 dots, and select *Redownload*
* Now **very important**, toggle the switch, *Show beta version* to On.
* The system will think a bit, and should then contain a list with Beta and Released version.
* Find the latest Beta version and click *Download*
* Once completed, restart Home Assistant
* When the system comes back, follow instructions in the [CONFIGURATION](#CONFIGURATION) section


## PRE-WORK

This integration uses the `entity_picture` attribute, which means you can get nice looking Pictograms instead of Icons on your dashboard. If you want to use this feature, do the following:
* download the file `renoweb_images.zip` from the [latest relase](https://github.com/briis/renoweb/releases) and unzip the content. You should see a folder called `renoweb` with a bunch of `.svg` in it.
* Open a file share to the `config` share on your Home Assistant entity, and go to the `www` directory. If this directory does not exist, just create it.
* Now copy the folder `renoweb` from the Zip file to the `www` directory and that is it. This is where this integration will look for the Entity Pictures.

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

## CONFIGURATION

In order to add this Integration to Home Assistant, go to *Settings* and *Integrations*. If you just installed RenoWeb, do a Hard Refresh in your browser, while on this page, to ensure the Integration shows up.

Now click the **+** button in the lower right corner, and then search for *Renoweb*. That should bring up the below screen:

![](https://github.com/briis/renoweb/blob/main/images/documentation/config_flow.png)

Now fill out the form and click the *SEND* button. The Integration should now find all data for your address and add the available sensors to Home Assistant.



