# Enumeration of statuses
from enum import Enum, auto

class AccessError(Enum):
    KEY_ERROR = auto()
    TYPE_ERROR = auto()
    NONE = None
