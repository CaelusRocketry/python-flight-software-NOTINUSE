# Enumeration of statuses
from enum import Enum, auto

class Error(Enum):
    # No error
    NONE = auto()
    
    # Invalid packets
    INVALID_HEADER_ERROR = auto()
    INVALID_ARGUMENT_ERROR = auto()

    # Valve and sensor request errors
    REQUEST_ERROR = auto()