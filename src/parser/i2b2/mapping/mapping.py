from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import List


ResourceType = Enum("ResourceType", "Patient Observation Encounter", module=__name__)


@dataclass
class ItemRepr:
    system: str
    code: str
    param: str
    res: ResourceType


class Mapping(ABC):
    def __init__(self, file: str):
        self.file: str = file

    def lookup(self, item_key: str) -> List[ItemRepr]:
        pass


print(list(ResourceType))
