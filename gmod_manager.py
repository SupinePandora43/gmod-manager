import os
from Utils import Arguments, Config  # noqa F403
from Utils.steam import Steam
import json

config = Config(Arguments())
# create addons.json if doesn't exists
if not os.path.exists("addons.json"):
    with open("addons.json", "w") as addonsFile:
        addonsFile.write(
            json.dumps(
                {"addons": [], "dupes": [], "saves": [], "collections": []}, indent=4
            )
        )
        addonsFile.close()
# read addons.json
with open("addons.json", "r") as addonsFile:
    addons = dict(json.loads(addonsFile.read()))
    addonsFile.close()


def dedupe():
    for category in ["addons", "dupes", "saves", "collections"]:
        for i in range(len(addons[category])):
            for i1 in range(len(addons[category])):
                if i != i1:
                    try:
                        addon = addons[category][i]
                        addon1 = addons[category][i1]
                        if (
                            (addon["title"] == addon1["title"])
                            and (addon["description"] == addon1["description"])
                            and (addon["preview"] == addon1["preview"])
                            and (addon["url"] == addon1["url"])
                            and (addon["time_updated"] == addon1["time_updated"])
                        ):
                            if addon["childrens"] or addon1["childrens"]:
                                if addon["childrens"] and not addon1["childrens"]:
                                    del addons[category][i1]
                                elif not addon["childrens"] and addon1["childrens"]:
                                    del addons[category][i]
                            else:
                                del addons[category][i1]
                    except Exception:
                        pass


dedupe()

for addon in addons["addons"]:
    addonURL = addon["url"]
    addonTimeUpdated = addon["time_updated"]
    addonSTEAM = Steam(config, addonURL, addonTimeUpdated)
    addon["title"] = addonSTEAM.title
    addon["description"] = addonSTEAM.description
    addon["preview"] = addonSTEAM.previewURL
    addon["url"] = addonSTEAM.url
    addonSTEAM.install()
    addon["time_updated"] = addonSTEAM.latestUpdate_time

dedupe()

with open("addons.json", "w") as addonsFile:
    addonsFile.write(json.dumps(addons, indent=4))
    addonsFile.close()

# import requests
# from PIL import Image
# import numpy as np
# import os

# image_url: str = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png"
# img: Image.Image = Image.open(requests.get(image_url, stream=True).raw)

# img


# def toAscii(img, SC=0.36, GCF=7 / 4, WCF=2.5):
#     chars = np.asarray(list(" .,:;irsXA253hMHGS#9B&@"))
#     S = (round(img.size[0] * SC * WCF), round(img.size[1] * SC))
#     img = np.sum(np.asarray(img.resize(S)), axis=2)
#     img -= img.min()
#     img = (1.0 - img / img.max()) ** GCF * (chars.size - 1)
#     print("\n".join(("".join(r) for r in chars[img.astype(int)])))


# try:
#     size = os.get_terminal_size()
# except WindowsError:
#     pass

# toAscii(img, size.columns / 496)


# os.get_terminal_size(columns=149, lines=23)
# toAscii(img, 0.36, 7/4,             2.24)
#              496.6666666666667      10.267857142857142
