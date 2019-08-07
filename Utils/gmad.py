from subprocess import check_output
from Utils import Config


class Gmad:
    def __init__(self, config: Config, original: str, target: str):
        check_output([config.gmad, "extract", "-file", original, "-out", target])

    @staticmethod
    def download():
        import platform
        import requests
        import subprocess

        if platform.system() == "Windows":
            with open("./gmad.exe", "wb") as gmad_windows_file:
                gmad_windows_file.write(
                    requests.get(
                        "https://github.com/SupinePandora43/gmod-manager/releases/download/0.1.0/gmad.exe"
                    ).content
                )
                gmad_windows_file.close()
            gmad_path = "./gmad.exe"
        elif platform.system() == "Linux":
            gmad_linux = requests.get(
                "https://github.com/AbigailBuccaneer/gmad-build/releases/download/v20180201/gmad_linux"
            ).content
            with open("./gmad_linux", "wb") as gmad_linux_file:
                gmad_linux_file.write(gmad_linux)
                gmad_linux_file.close()
            gmad_linux = None
            gmad_path = "./gmad_linux"
            subprocess.check_output(["chmod", "+x", gmad_path])
        elif platform.system() == "Darwin":
            print("ГОВНО-ОС НЕ ПОДДЕРЖИВАЕМ!!!")
            print("SHIT-OS DONT SUPPORTING!!!")
        else:
            print(platform.system() + " - Platform can't be identified")
