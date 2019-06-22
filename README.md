# Gmod Manager
[![Build Status](https://travis-ci.com/SupinePandora43/gmod-manager.svg?branch=master)](https://travis-ci.com/SupinePandora43/gmod-manager)
## Features
* ### Supports
  * Addons
  * Dupes
  * Saves
  * Collections
* Download only if update available
* Download progress
* Custom configuration (main.cfg)
## How-To-Use
1. change paths in main.cfg (`gmad_path`, `gmod_path`, `temp_path`)
2. enter in command line/prompt `python main.py -install` (steam workshop link)
## Arguments
* `-install` - argumant for providing workshop urls/id's. `python main.py -install https://steamcommunity.com/sharedfiles/filedetails/?id=1771611119`
* `-nocheck` - argument for disabling checking for updates, addons in addons.json. `python main.py -nocheck -install https://steamcommunity.com/sharedfiles/filedetails/?id=1771611119`
## Requirements
* Python 3
## Limitations
* finds addons.json only in script folder
* can't download collections through `-install` argument

inspired by https://github.com/magnusjjj/gmadget
