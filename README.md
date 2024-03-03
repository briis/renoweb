# Garbage Collection DK

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![Community Forum][forum-shield]][forum]


The renoweb integration adds support for retreiving Garbage Collection data from Municipalities around Denmark. The integration uses the same lookup API's as the Municipalities do, so if your Municipality uses Renoweb as their data API, there is very good chance that this integration will work for you.

The biggest issue is that there is NO standard for the way municipalities mix the content of containers. Some have glas & metal in one container, others have glas and paper in one container, etc and also even though they do mix the same content in a container, they do not name it the same. In order to have some structure I need them grouped together and this is a bit of a challenge with all these different types. If a new pickup-type is found, the system will log a warning, which you can put in an issue and I will add it to the list. Please enable logging for the wrapper module in Home assistant to get this warning in Home Assistant, by adding this code to your `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.renoweb: error
    pyrenoweb: error
```

### This integration will set up the following platforms.

Platform | Description
-- | --
`sensor` | A Home Assistant `sensor` entity, with all available sensor from the API. State value will be the days until next pick-up
`calendar` | An entry will be made in to a local Home Assistant `calendar`. There will be a full-day event every time there is a pick-up, describing what is collected.


## NOT ALL MUNICIPALTIES ARE SUPPORTED
Unfortunately not all Municipalities use the API I use here, and therefore they are NOT supported, and CANNOT be added to the list. I have been through all Municipalities and I found 47 of them to work with this API. There are a few more who seem to have access to the API, but they have decided on a very different implementation.

Go to the [Municipality List](#MUNICIPALITIES) to see if your Municipality will work with this integration

**PLEASE RAISE AN ISSUE IF YOU CAN SELECT YOUR MUNICIPALITY BUT THE ADDRESS DOES NOT WORK**

The same applies if you can get data, but are missing one or more items that should have been on the Pick-Up list.

## CREDITS

A big thank you to @thomaspalmdk for finding the new API, and help test this new version.

## UPGRADING FROM VERSION 1.X

As stated above, as of version 2.0, I am using a completely new API, and I have also used the opportunity to ensure this Integration delivers on the latest Home Assistant Requirements. All this means that there is NO direct upgrade path from V1.x to this Version and all your sensors will get new names and new Unique ID's, which again means you will have to change automations, scripts and dashboard after installing this version.

If you never installed Renoweb before go directly the [Installation section](#INSTALLATION).

Here is the suggested *"Upgrade"* Procedure:

#### Remove your current Renoweb setup
1. Go to *Settings* | *Devices & Services
2. Click on *Renoweb Garbage Collection*
3. Click on the 3 dots to the right of each address you installed, and click *Delete*


#### Add Renoweb V2.0 to your system
* **This only applies while we are running the Beta, after that just you the normal Installation/Upgrade procedures**
* Go to *HACS* and then click on *Integrations*
* Find *Renoweb Garbage Collection* and click on it.
* In the upper right corner, click on the 3 dots, and select *Redownload*
* Now **very important**, toggle the switch, *Show beta version* to On.
* The system will think a bit, and should then contain a list with Beta and Released version.
* Find the latest Beta version and click *Download*
* Once completed, restart Home Assistant
* When the system comes back, follow instructions in the [CONFIGURATION](#CONFIGURATION) section


## PRE-WORK

This integration uses the `entity_picture` attribute, which means you can get nice looking Pictograms instead of Icons on your dashboard. If you want to use this feature, do the following:
* Download the file `renoweb_images.zip` from the [latest relase](https://github.com/briis/renoweb/releases) and unzip the content. (Find the **Assets** link in the bottom of the release and click it to unfold) You should see a file called `renoweb_images` with a bunch of `.svg` files in it.
* Open a file share to the `config` share on your Home Assistant entity, and go to the `www` directory. If this directory does not exist, just create it.
* Now create a folder called `renoweb` in the `www` directory and copy all the `.svg` files to this directory. This is where this integration will look for the Entity Pictures.

## INSTALLATION

### HACS Installation

This Integration is not part of the default HACS store, but you can add it as a Custom repository in HACS by doing the following:

1. Go to HACS in your HA installation, and click on *Integrations*
2. Click the three vertical dots in the upper right corner, and select *Custom repositories*
3. Add `https://github.com/briis/renoweb` and select *Integration* as Category, and then click *Add*

You should now be able to find this Integration in HACS. After the installation of the files, you must restart Home Assistant, or else you will not be able to add Renoweb from the Integration Page.

If you are not familiar with HACS, or haven't installed it, I would recommend to [look through the HACS documentation](https://hacs.xyz/), before continuing. Even though you can install the Integration manually, I would recommend using HACS, as you would always be reminded when a new release is published.

### Manual Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `renoweb`.
4. Download _all_ the files from the `custom_components/renoweb/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Renoweb"

## CONFIGURATION

To add Renoweb to your installation, do the following:

- Go to Configuration and Integrations
- Click the + ADD INTEGRATION button in the lower right corner.
- Search for *Renoweb* and click the integration.
- When loaded, there will be a configuration box, where you must enter:

  | Parameter | Required | Default Value | Description |
  | --------- | -------- | ------------- | ----------- |
  | `Municipality` | Yes | None | Select your Municipality from the Dropdown list. You can press the first letter of your municipality to quickly scroll down. |
  | `Road name` | Yes | None | Type the name of the road you want to get collection data for. Without house number. |
  | `House Number` | Yes | None | The house number of the address. Also accepts letters. If you have a house number like 2A or similar, and it does not work, try putting a space between the number and the letter, like 2 A |

- Click on SUBMIT to save your data. If all goes well you should now have a two new entities under the Renoweb integration


You can configure more than 1 instance of the Integration by using a different Address.


## MUNICIPALITIES

Here is the list of currently supported Municipalities

    - Aabenraa
    - Aalborg
    - Albertslund
    - Allerød
    - Brøndby
    - Brønderslev
    - Dragør
    - Egedal
    - Esbjerg
    - Faxe
    - Fredensborg
    - Frederiksberg
    - Frederikssund
    - Furesø
    - Gentofte
    - Gladsaxe
    - Glostrup
    - Greve
    - Gribskov
    - Halsnæs
    - Hedensted
    - Helsingør
    - Herlev
    - Hillerød
    - Hjørring
    - Horsens
    - Hvidovre
    - Høje-Taastrup
    - Hørsholm
    - Jammerbugt
    - Kerteminde
    - Køge
    - Lyngby-Taarbæk
    - Mariagerfjord
    - Næstved
    - Odsherred
    - Randers
    - Rebild
    - Ringkøbing-Skjern
    - Ringsted
    - Roskilde
    - Rødovre
    - Samsø
    - Slagelse
    - Solrød
    - Sorø
    - Stevns
    - Svendborg
    - Sønderborg
    - Tårnby
    - Varde
    - Vejen
    - Vordingborg

***

[commits-shield]: https://img.shields.io/github/commit-activity/y/briis/renoweb.svg?style=flat-square
[commits]: https://github.com/briis/renoweb/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=flat-square
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/briis/renoweb.svg?style=flat-square
[maintenance-shield]: https://img.shields.io/badge/maintainer-Bjarne%20Riis%20%40briis-blue.svg?style=flat-square
[releases-shield]: https://img.shields.io/github/release/briis/renoweb.svg?include_prereleases&style=flat-square&style=flat-square
[releases]: https://github.com/briis/renoweb/releases