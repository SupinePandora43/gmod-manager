from abc import abstractmethod, ABCMeta
from .config import Config
from typing import Any


class IModification(metaclass=ABCMeta):
    title: str = ""
    valid: bool = False

    @abstractmethod
    def __init__(self, config: Config, identifier: str, time_updated: Any):
        pass

    @abstractmethod
    def isLatest(self):
        raise NotImplementedError

    @abstractmethod
    def install(self):
        raise NotImplementedError
