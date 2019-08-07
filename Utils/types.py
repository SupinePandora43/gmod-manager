from .steam import Steam
from .git import Git
from .Imodification import IModification
from typing import Union, Any
import re


class Types:
    STEAM = Steam
    GIT = Git
    INVALID = None

    @staticmethod
    def getType(identifier: str) -> Union[IModification, Any]:
        if re.match(
            r"((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?)",
            identifier,
        ):
            return Types.GIT
        elif re.match(
            r"((http(s)?)(:(//)?)(steamcommunity.com)(/.*/.*/)(.*)(id=)\d*)", identifier
        ):
            return Types.STEAM
        else:
            return Types.INVALID
