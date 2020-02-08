# Enumeration of statuses
from enum import Enum

class SetError(Enum):
    KEY_ERROR = auto()
    TYPE_ERROR = auto()
    NONE = auto()

class Error(Enum):
    ERROR