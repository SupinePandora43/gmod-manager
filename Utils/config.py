import os
from configparser import ConfigParser
from .arguments import Arguments
from typing import Union


class Config:
    config: Union[ConfigParser, None] = None
    gmad = ""
    args: Union[Arguments, None] = None
    temp = ""
    gmod = ""

    def __init__(self, args: Arguments):
        self.args = args
        self.config = ConfigParser()
        if not os.path.exists("main.cfg"):
            self.config.add_section("main")
            for gmad_probably_path in [
                "./gmad.exe",
                "../bin/gmad.exe",
                "./gmad_linux",
                "./gmad",
                "../bin/gmad",
                "../bin/gmad_linux",
            ]:
                if os.path.exists(gmad_probably_path):
                    self.gmad = gmad_probably_path
            self.config.set("main", "gmad_path", str(self.gmad))
            self.config.set("main", "temp_path", "temp")
            self.config.set("main", "gmod_path", ".")
            with open("main.cfg", "w") as configFile:
                self.config.write(configFile)
                configFile.close()
        else:
            self.config.read("main.cfg")
        self.gmad = self.config.get("main", "gmad_path")
        self.temp = self.config.get("main", "temp_path")
        self.gmod = self.config.get("main", "gmod_path")
        self.check_paths()

    def check_paths(self):
        folders = ["addons", "dupes", "saves"]
        if not os.path.exists(self.config.get("main", "temp_path")):
            os.makedirs(self.config.get("main", "temp_path"))
        for folder in folders:
            if not os.path.exists(self.config.get("main", "gmod_path") + "/" + folder):
                os.makedirs(self.config.get("main", "gmod_path") + "/" + folder)
