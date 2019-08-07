from typing import List
import argparse


class Arguments:
    extract = True
    download_gmad = False
    check = True
    install: List[str] = []

    def __init__(self):
        parser = argparse.ArgumentParser(description="Tool for managing Gmod content")
        parser.add_argument("-noextract", help="for travis", action="store_true")
        parser.add_argument("-download", help="Download gmad", action="store_true")
        parser.add_argument(
            "-nocheck",
            help="Install/Check content only provided via 'install' arg",
            action="store_true"
        )
        parser.add_argument(
            "-install", help="Install new content", type=str, nargs="+", metavar="ID"
        )
        args = vars(parser.parse_args())
        self.extract = not args["noextract"]
        self.download_gmad = args["download"]
        self.check = not args["nocheck"]
        self.install = args["install"]
