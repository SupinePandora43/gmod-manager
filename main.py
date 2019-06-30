import requests
import os
import argparse
import json
import lzma
import subprocess
import shutil
import sys
from configparser import ConfigParser

config = ConfigParser()
if not os.path.exists("main.cfg"):
    config.add_section("main")
    gmad_path = "gmad.exe"
    import platform
    if platform.system() == "Windows":
        if os.path.exists("../bin/gmad.exe"):
            gmad_path = "../bin/gmad.exe"
        else:
            try:
                if not "Garry's Mod Addon Creator" in str(subprocess.check_output("gmad.exe")):
                    with open("./gmad.exe", "wb") as gmad_windows_file:
                        gmad_windows_file.write(requests.get(
                            "https://github.com/SupinePandora43/gmod-manager/releases/download/0.1.0/gmad.exe").content)
                        gmad_windows_file.close()
            except FileNotFoundError as err:
                pass
    elif platform.system() == "Linux":
        passed = False
        for gmad_probably_path in ["./gmad_linux", "./gmad", "../bin/gmad", "../bin/gmad_linux"]:
            if os.path.exists(gmad_probably_path):
                gmad_path = gmad_probably_path
                passed = True
        if not passed:
            gmad_linux = requests.get(
                "https://github.com/AbigailBuccaneer/gmad-build/releases/download/v20180201/gmad_linux").content
            with open("./gmad_linux", "wb") as gmad_linux_file:
                gmad_linux_file.write(gmad_linux)
                gmad_linux_file.close()
            gmad_linux = None
            gmad_path = "./gmad_linux"
            subprocess.check_output(["chmod", "+x", gmad_path])
    elif platform.system() == "Darwin":
        pass
    else:
        print(platform.system() + " - Platform can't be identified")
    config.set("main", "gmad_path", gmad_path)
    config.set("main", "temp_path", "temp")
    config.set("main", "gmod_path", ".")
    with open("main.cfg", "w") as configFile:
        config.write(configFile)
        configFile.close()
else:
    config.read("main.cfg")

folders = [
    "addons", "dupes", "saves"
]
if not os.path.exists(config.get("main", "temp_path")):
    os.makedirs(config.get("main", "temp_path"))
for folder in folders:
    if not os.path.exists(config.get("main", "gmod_path")+"/" + folder):
        os.makedirs(config.get("main", "gmod_path")+"/" + folder)

headers = {
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "text/plain"
}


class url_parser():
    def getID(url):
        import urllib.parse
        steamID = urllib.parse.parse_qsl(url)[0][1]
        return steamID


class valid_fileName_generator():
    fileName = None

    def __init__(self, title):
        """
        generates valid fileName from steam workshop title

        original code: https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8
        """
        import unicodedata
        import string
        valid_filename_chars = "-_.[]() %s%s" % (string.ascii_letters, string.digits)
        for r in ' ':
            title = title.replace(r, '_')
        self.fileName = unicodedata.normalize(
            'NFKD', title).encode('ASCII', 'ignore').decode()
        self.fileName = ''.join(
            c for c in self.fileName if c in valid_filename_chars)
        self.fileName = self.fileName[:255]


class steam_object():
    url = None
    steamID = None
    collectionResult = None
    fileResult = None
    collectionJSON = None
    fileJSON = None
    time_updated = None
    directURL = None
    previewURL = None
    description = None
    title = None
    latestUpdate_time = None

    def __init__(self, url="", time_updated=0):
        self.url = url
        self.steamID = url_parser.getID(self.url)
        self.time_updated = time_updated
        self.url = "https://steamcommunity.com/sharedfiles/filedetails/?id=" + \
            str(self.steamID)
        self.request()

    def request(self):
        self.collectionResult = requests.post(
            "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v0001/",
            "collectioncount=1&publishedfileids[0]="+str(self.steamID),
            headers=headers)
        self.fileResult = requests.post(
            "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v0001/",
            "itemcount=1&publishedfileids[0]="+str(self.steamID),
            headers=headers)
        self.collectionJSON = json.loads(self.collectionResult.text)
        self.fileJSON = json.loads(self.fileResult.text)
        if self.steam_type() != None:
            self.title = self.fileJSON['response']['publishedfiledetails'][0]['title']
            self.description = self.fileJSON['response']['publishedfiledetails'][0]['description']
            self.directURL = self.fileJSON['response']['publishedfiledetails'][0]['file_url']
            self.previewURL = self.fileJSON['response']['publishedfiledetails'][0]['preview_url']
            self.latestUpdate_time = self.fileJSON['response']['publishedfiledetails'][0]['time_updated']

    def isLatest(self):
        if self.latestUpdate_time <= self.time_updated:
            return True
        else:
            return False

    def steam_type(self):

        if len(self.fileJSON['response']['publishedfiledetails'][0]) <= 2:
            return None
        elif "addon" in str(self.fileJSON['response']['publishedfiledetails'][0]['filename']) or "gm" in str(self.fileJSON['response']['publishedfiledetails'][0]['filename']):
            return "addon"
        elif str(self.fileJSON["response"]["publishedfiledetails"][0]["filename"]).startswith("creation/"):
            if str(self.fileJSON['response']['publishedfiledetails'][0]['tags'][0]['tag']) == "Dupe":
                return "dupe"
            elif(str(self.fileJSON['response']['publishedfiledetails'][0]['tags'][0]['tag']) == "Save"):
                return "save"
        elif not self.collectionJSON['response']['collectiondetails'][0]['result'] == 9:
            return "collection"


# create addons.json if doesn't exists
if not os.path.exists("addons.json"):
    with open("addons.json", "w") as addonsFile:
        addonsFile.write(json.dumps(
            {"addons": [], "dupes": [], "saves": [], "collections": []}, indent=4))
        addonsFile.close()
# read addons.json
with open("addons.json", "r") as addonsFile:
    addons = dict(json.loads(addonsFile.read()))
    addonsFile.close()

nogmad = False


def dedupe():
    for category in ["addons", "dupes", "saves", "collections"]:
        for i in range(len(addons[category])):
            for i1 in range(len(addons[category])):
                if i != i1:
                    try:
                        addon = addons[category][i]
                        addon1 = addons[category][i1]
                        if (addon["title"] == addon1["title"]) and (addon["description"] == addon1["description"]) and (addon["preview"] == addon1["preview"]) and (addon["url"] == addon1["url"]) and (addon["time_updated"] == addon1["time_updated"]):
                            if addon["childrens"] or addon1["childrens"]:
                                if addon["childrens"] and not addon1["childrens"]:
                                    del addons[category][i1]
                                elif not addon["childrens"] and addon1["childrens"]:
                                    del addons[category][i]
                            else:
                                del addons[category][i1]
                    except:
                        pass


def extract(steam_obj: steam_object):
    path = config.get("main", "temp_path")+"/" + \
        valid_fileName_generator(steam_obj.title).fileName
    with lzma.open(path) as f:
        with open(path + ".extracted", "wb+") as fout:
            fout.write(f.read())
            fout.close()
        f.close()


def installed(steam_obj: steam_object):
    if steam_obj.steam_type() == "addon":
        return os.path.exists(config.get("main", "gmod_path")+"/addons/"+valid_fileName_generator(steam_obj.title).fileName)
    elif steam_obj.steam_type() == "dupe":
        return os.path.exists(config.get("main", "gmod_path")+"/dupes/"+valid_fileName_generator(steam_obj.title).fileName+".dupe")
    elif steam_obj.steam_type() == "save":
        return os.path.exists(config.get("main", "gmod_path")+"/saves/"+valid_fileName_generator(steam_obj.title).fileName+".gms")


def install_not_collection(steam_obj: steam_object, collection: str = None, latest=False):
    prefix = ""
    indent = ""
    if collection:
        prefix = "├"
        indent = "│ "
        if latest:
            prefix = "└"
            indent = " "
    print(prefix + steam_obj.title)
    if (not steam_obj.isLatest()) or (not installed(steam_obj)):
        # print(indent+"├ downloading")
        r = requests.get(steam_obj.directURL, stream=True)
        with open(config.get("main", "temp_path")+"/"+valid_fileName_generator(steam_obj.title).fileName, "wb") as workshopFile:
            total_length = r.headers.get('content-length')
            if total_length is None:
                workshopFile.write(r.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in r.iter_content(chunk_size=4096):
                    dl += len(data)
                    workshopFile.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r"+indent+"├ downloading [%s%s]" %
                                     ('=' * done, '─' * (50-done)))
                    sys.stdout.flush()
                print("")
            workshopFile.close()
        print(indent + "├ extracting")
        extract(steam_obj)
        os.remove(config.get("main", "temp_path")+"/" +
                  valid_fileName_generator(steam_obj.title).fileName)
        if steam_obj.steam_type() == "addon":
            print(indent + "└ extracting via gmad")
            if not nogmad:
                subprocess.check_output([config.get("main", "gmad_path"), "extract", "-file", config.get("main", "temp_path")+"/" +
                                         valid_fileName_generator(steam_obj.title).fileName + ".extracted", "-out", config.get("main", "gmod_path")+"/addons/"+valid_fileName_generator(steam_obj.title).fileName])
        elif steam_obj.steam_type() == "dupe":
            shutil.copy(config.get("main", "temp_path")+"/"+valid_fileName_generator(steam_obj.title).fileName + ".extracted",
                        config.get("main", "gmod_path")+"/dupes/"+valid_fileName_generator(steam_obj.title).fileName+".dupe")
            preview = requests.get(steam_obj.previewURL)
            with open(config.get("main", "gmod_path")+"/dupes/"+valid_fileName_generator(steam_obj.title).fileName + ".jpg", "wb") as previewFile:
                previewFile.write(preview.content)
                previewFile.close()
        elif steam_obj.steam_type() == "save":
            shutil.copy(config.get("main", "temp_path")+"/"+valid_fileName_generator(steam_obj.title).fileName + ".extracted",
                        config.get("main", "gmod_path")+"/saves/"+valid_fileName_generator(steam_obj.title).fileName+".gms")
            preview = requests.get(steam_obj.previewURL)
            with open(config.get("main", "gmod_path")+"/saves/"+valid_fileName_generator(steam_obj.title).fileName + ".jpg", "wb") as previewFile:
                previewFile.write(preview.content)
                previewFile.close()
        os.remove(config.get("main", "temp_path")+"/" +
                  valid_fileName_generator(steam_obj.title).fileName + ".extracted")
    else:
        print(indent + "└ latest")


def install_collection(steam_obj: steam_object):
    print(steam_obj.title)
    newTimes = {}
    for iID in range(len(steam_obj.collectionJSON['response']['collectiondetails'][0]['children'])):
        addon = steam_obj.collectionJSON["response"]['collectiondetails'][0]["children"][iID]
        try:
            newTimes[addon["publishedfileid"]
                     ] = collection["childrens"][addon["publishedfileid"]]
        except:
            newTimes[addon["publishedfileid"]] = 0
        addonSTEAM = steam_object(
            "https://steamcommunity.com/sharedfiles/filedetails/?id="+addon["publishedfileid"], newTimes[addon["publishedfileid"]])
        install(addonSTEAM, collection=steam_obj.title, latest=(iID == len(
            steam_obj.collectionJSON['response']['collectiondetails'][0]['children'])-1))
        newTimes[addon["publishedfileid"]] = addonSTEAM.latestUpdate_time

    return {"childrens": newTimes}


def install(steam_obj: steam_object, collection: str = None, latest=False):
    if steam_obj.steam_type() == "collection":
        return install_collection(steam_obj)
    elif not steam_obj.steam_type() == None:
        install_not_collection(steam_obj, collection, latest)
    else:
        print("ERROR: " + steam_obj.url + ", isn't valid")


parser = argparse.ArgumentParser(
    description='Tool for managing Gmod Steam content')
parser.add_argument("-nogmad", help="for travis", action="store_true")
parser.add_argument("-nocheck",
                    help="Install/Check content only provided via 'install' arg", action="store_true")

parser.add_argument("-install",
                    help="Install new content", type=str, nargs='+', metavar='ID')
args = vars(parser.parse_args())


def installARGS(url):
    """
    thanks https://stackoverflow.com/a/43424173/9765252
    """
    new_steam_object = steam_object(url)
    category = addons[new_steam_object.steam_type() + "s"]
    install(new_steam_object)
    new_object = {"title": new_steam_object.title,
                  "description": new_steam_object.description,
                  "preview": new_steam_object.previewURL,
                  "url": new_steam_object.url,
                  "time_updated": new_steam_object.latestUpdate_time}
    category.insert(0, new_object)
    dedupe()


nogmad = args["nogmad"]

if args["install"]:
    for steam in args["install"]:
        if str(steam).isdigit():
            installARGS(
                "https://steamcommunity.com/sharedfiles/filedetails/?id="+steam)
        elif str(steam):
            installARGS(steam)
        else:
            pass

if not args["nocheck"]:
    for addon in addons["addons"]:
        addonURL = addon["url"]
        addonTimeUpdated = addon["time_updated"]
        addonSTEAM = steam_object(addonURL, addonTimeUpdated)
        addon["title"] = addonSTEAM.title
        addon["description"] = addonSTEAM.description
        addon["preview"] = addonSTEAM.previewURL
        addon["url"] = addonSTEAM.url
        install(addonSTEAM)
        addon["time_updated"] = addonSTEAM.latestUpdate_time

    for dupe in addons["dupes"]:
        dupeURL = dupe["url"]
        dupeTimeUpdated = dupe["time_updated"]
        dupeSTEAM = steam_object(dupeURL, dupeTimeUpdated)
        dupe["title"] = dupeSTEAM.title
        dupe["description"] = dupeSTEAM.description
        dupe["preview"] = dupeSTEAM.previewURL
        dupe["url"] = dupeSTEAM.url
        install(dupeSTEAM)
        dupe["time_updated"] = dupeSTEAM.latestUpdate_time

    for save in addons["saves"]:
        saveURL = save["url"]
        saveTimeUpdated = save["time_updated"]
        saveSTEAM = steam_object(saveURL, saveTimeUpdated)
        save["title"] = saveSTEAM.title
        save["description"] = saveSTEAM.description
        save["preview"] = saveSTEAM.previewURL
        save["url"] = saveSTEAM.url
        install(saveSTEAM)
        save["time_updated"] = saveSTEAM.latestUpdate_time
    dedupe()
    for collection in addons["collections"]:
        steam_obj = steam_object(
            collection["url"], collection["time_updated"])
        collection["url"] = steam_obj.url
        collection["title"] = steam_obj.title
        collection["description"] = steam_obj.description
        collection["preview"] = steam_obj.previewURL
        result = install_collection(steam_obj)
        collection["time_updated"] = steam_obj.latestUpdate_time
        collection["childrens"] = result["childrens"]

# for i in range(len(addons["collections"])):
#     collection = addons["collections"][i]
#     collectionSTEAM = steam_object(collection["url"])
#     for addon in collectionSTEAM.collectionJSON['response']['collectiondetails'][0]['"children"']:
#         addonSTEAM = steam_object(
#             "https://steamcommunity.com/sharedfiles/filedetails/?id="+addon["publishedfileid"])
#         print(addonSTEAM.title)
#         addons['collections'][i]['children'][addonSTEAM.steamID] = addonSTEAM.latestUpdate_time

dedupe()

with open("addons.json", "w") as addonsFile:
    addonsFile.write(json.dumps(addons, indent=4))
    addonsFile.close()
# https://steamcommunity.com/sharedfiles/filedetails/?id=1716648512 dupe
# https://steamcommunity.com/sharedfiles/filedetails/?id=1767675383 save
# https://steamcommunity.com/sharedfiles/filedetails/?id=675560712  addon
