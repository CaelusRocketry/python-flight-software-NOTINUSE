# Enumeration of statuses
from enum import Enum, auto

class SetError(Enum):
    KEY_ERROR = auto()
    TYPE_ERROR = auto()
    NONE = auto()
