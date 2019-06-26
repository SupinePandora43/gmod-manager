# Gmod Manager

[![Build Status](https://travis-ci.com/SupinePandora43/gmod-manager.svg?branch=master)](https://travis-ci.com/SupinePandora43/gmod-manager)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FSupinePandora43%2Fgmod-manager.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FSupinePandora43%2Fgmod-manager?ref=badge_shield)

- [Gmod Manager](#Gmod-Manager)
  - [Features](#Features)
  - [How To Install](#How-To-Install)
  - [Arguments](#Arguments)
  - [Paths](#Paths)
  - [Build Requirements](#Build-Requirements)
  - [Limitations](#Limitations)
  - [License](#License)

## Features

- ### Supports

  - Addons
  - Dupes
  - Saves
  - Collections
- Download only if update available
- Download progress
- Custom configuration (main.cfg)

## How To Install

1. download exe from [releases](https://github.com/SupinePandora43/gmod-manager/releases)
2. move `gmod-manager.exe` to `Garry's Mod/garrysmod` folder, run it!
3. change [paths](#Paths) in `main.cfg`
4. enter in command line/prompt `gmod-manager.py -install` (steam workshop link)

## Arguments

- `-install` - argument for providing workshop urls/id's. `python main.py -install https://steamcommunity.com/sharedfiles/filedetails/?id=1771611119`
- `-nocheck` - argument for disabling checking for updates, addons in addons.json. `python main.py -nocheck -install https://steamcommunity.com/sharedfiles/filedetails/?id=1771611119`

## Paths

| Path        | Optional                 | Description         | Default value                                      |
| ----------- | ------------------------ | ------------------- | -------------------------------------------------- |
| `gmad_path` | :heavy_multiplication_x: | path to `gmad.exe`  | `gmad.exe` ( if in gmod folder: `../bin/gmad.exe`) |
| `temp_path` | :heavy_check_mark:       | temp folder         | `temp`                                             |
| `gmod_path` | :heavy_check_mark:       | path to `garrysmod` | `.`                                                |

## Build Requirements

- Python 3

## Limitations

- uses addons.json only in self folder
- can't dedupe collections

inspired by [magnusjjj/gmadget](https://github.com/magnusjjj/gmadget)

## License

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FSupinePandora43%2Fgmod-manager.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FSupinePandora43%2Fgmod-manager?ref=badge_large)
