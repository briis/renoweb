# Garbage Collection DK

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![Community Forum][forum-shield]][forum]


The renoweb integration adds support for retreiving Garbage Collection data from Municipalities around Denmark. The integration uses the same lookup API's as the Municipalities do, so if your Municipality uses RenoWeb as their data API, there is very good chance that this integration will work for you.

#### This integration will set up the following platforms.

Platform | Description
-- | --
`sensor` | A Home Assistant `sensor` entity, with all available sensor from the API. State value will be the days until next pick-up
`calendar` | An entry will be made in to a local Home Assistant `calendar`. There will be a full-day event every time there is a pick-up, describing what is collected.


## MUNICIPALTIES NOT SUPPORTED
Unfortunately not all Municipalities use the API I use here, and therefore they are NOT supported, and CANNOT be added to the list.

As of writing this, I have found the following Municipalities to NOT work:
* Fåborg-Midtfyn
* København
* Århus

**PLEASE RAISE AN ISSUE IF YOU CAN SELECT YOUR MUNICIPALITY BUT THE ADDRESS DOES NOT WORK**

I have not testet all municipalities that are still on the list, and I cannot guarantee that all will work. If you find that your Municipality and address does not work, please create an issue here on Github. I can then investigate if it is correctable, or I need to add the Municpality to the above list.

The same applies if you can get data, but are missing one or more items that should have been on the Pick-Up list.

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

You should now be able to find this Integration in HACS. After the installation of the files, you must restart Home Assistant, or else you will not be able to add RenoWeb from the Integration Page.

If you are not familiar with HACS, or haven't installed it, I would recommend to [look through the HACS documentation](https://hacs.xyz/), before continuing. Even though you can install the Integration manually, I would recommend using HACS, as you would always be reminded when a new release is published.

### Manual Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `renoweb`.
4. Download _all_ the files from the `custom_components/renoweb/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "WRenoWeb"

## CONFIGURATION

To add RenoWeb to your installation, do the following:

- Go to Configuration and Integrations
- Click the + ADD INTEGRATION button in the lower right corner.
- Search for *RenoWeb** and click the integration.
- When loaded, there will be a configuration box, where you must enter:

  | Parameter | Required | Default Value | Description |
  | --------- | -------- | ------------- | ----------- |
  | `Municipality` | Yes | None | Select your Municipality from the Dropdown list. You can press the first letter of your municipality to quickly scroll down. |
  | `Road name` | Yes | None | Type the name of the road you want to get collection data for. Without house number. |
  | `House Number` | Yes | None | The house number of the address. Also accepts letters. |

- Click on SUBMIT to save your data. If all goes well you should now have a two new entities under the RenoWeb integration


You can configure more than 1 instance of the Integration by using a different Address.




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