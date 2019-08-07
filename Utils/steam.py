from . import IModification, File, Config
from typing import Union
import requests
import json
import sys
import lzma
from enum import Enum
from .gmad import Gmad


def parse(identifier: Union[str, int] = "") -> int:
    try:
        return int(identifier)
    except ValueError:
        from urllib.parse import parse_qsl

        return int(parse_qsl(str(identifier))[0][1])
    except Exception:
        return -1


class Steam(IModification):
    url: str = ""
    steamID: int = -1
    collectionResult = None
    fileResult = None
    collectionJSON: dict = {}
    fileJSON: dict = {}
    time_updated: int = -1
    directURL: str = ""
    previewURL: str = ""
    description: str = ""
    latestUpdate_time: int = -1
    config: Union[Config, None] = None

    class Type(Enum):
        INVALID = None
        ADDON = "addon"
        DUPE = "dupe"
        SAVE = "save"
        COLLECTION = "collection"

    def __init__(self, config: Config, identifier: str, time_updated: int = -1):
        self.config = config
        self.steamID = parse(identifier)
        self.url = str(self.steamID)
        self.time_updated = time_updated
        self.url = "https://steamcommunity.com/sharedfiles/filedetails/?id=" + str(
            self.steamID
        )
        self.request()

    def request(self):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain",
        }
        self.collectionResult = requests.post(
            "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v0001/",
            "collectioncount=1&publishedfileids[0]=" + str(self.steamID),
            headers=headers,
        )
        self.fileResult = requests.post(
            "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v0001/",
            "itemcount=1&publishedfileids[0]=" + str(self.steamID),
            headers=headers,
        )
        self.collectionJSON = json.loads(self.collectionResult.text)
        self.fileJSON = json.loads(self.fileResult.text)
        self.checkValid()
        if self.valid:
            self.title = self.fileJSON["response"]["publishedfiledetails"][0]["title"]
            self.description = self.fileJSON["response"]["publishedfiledetails"][0][
                "description"
            ]
            self.directURL = self.fileJSON["response"]["publishedfiledetails"][0][
                "file_url"
            ]
            self.previewURL = self.fileJSON["response"]["publishedfiledetails"][0][
                "preview_url"
            ]
            self.latestUpdate_time = self.fileJSON["response"]["publishedfiledetails"][
                0
            ]["time_updated"]

    def checkValid(self):
        if self.steam_type() is not Steam.Type.INVALID:
            self.valid = True
        else:
            self.valid = False

    def steam_type(self):
        if len(self.fileJSON["response"]["publishedfiledetails"][0]) <= 2:
            return Steam.Type.INVALID
        elif "addon" in str(
            self.fileJSON["response"]["publishedfiledetails"][0]["filename"]
        ) or "gm" in str(
            self.fileJSON["response"]["publishedfiledetails"][0]["filename"]
        ):
            return Steam.Type.ADDON
        elif str(
            self.fileJSON["response"]["publishedfiledetails"][0]["filename"]
        ).startswith("creation/"):
            if (
                str(
                    self.fileJSON["response"]["publishedfiledetails"][0]["tags"][0][
                        "tag"
                    ]
                )
                == "Dupe"
            ):
                return Steam.Type.DUPE
            elif (
                str(
                    self.fileJSON["response"]["publishedfiledetails"][0]["tags"][0][
                        "tag"
                    ]
                )
                == "Save"
            ):
                return Steam.Type.SAVE
        elif not self.collectionJSON["response"]["collectiondetails"][0]["result"] == 9:
            return Steam.Type.COLLECTION

    def isLatest(self):
        if self.latestUpdate_time <= self.time_updated:
            return True
        else:
            return False

    def install(self):
        if self.valid:
            s_type = self.steam_type()
            print(self.title)
            if s_type is self.Type.ADDON:
                r = requests.get(self.directURL, stream=True)
                with open(
                    self.config.temp + "/" + File(self.title).fileName, "wb"
                ) as workshopFile:
                    total_length = r.headers.get("content-length")
                    if total_length is None:
                        workshopFile.write(r.content)
                    else:
                        dl = 0
                        total_length = int(total_length)
                        for data in r.iter_content(chunk_size=4096):
                            dl += len(data)
                            workshopFile.write(data)
                            done = int(50 * dl / total_length)
                            sys.stdout.write(
                                "\r"
                                + "├ downloading [%s%s]"
                                % ("=" * done, "─" * (50 - done))
                            )
                            sys.stdout.flush()
                        print("")
                    workshopFile.close()
                path = self.config.temp + "/" + File(self.title).fileName
                print("├ extracting")
                with lzma.open(path) as f:
                    with open(path + ".extracted", "wb+") as fout:
                        fout.write(f.read())
                        fout.close()
                    f.close()
                print("└ extracting via gmad")
                if self.config.args.extract:
                    Gmad(
                        self.config,
                        path + ".extracted",
                        self.config.gmod + "/addons/" + File(self.title).fileName,
                    )
            elif s_type is self.Type.DUPE:
                pass
            elif s_type is self.Type.SAVE:
                pass
            elif s_type is self.Type.COLLECTION:
                pass
        else:
            pass
