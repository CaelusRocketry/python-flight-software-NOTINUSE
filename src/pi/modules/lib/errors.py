# Enumeration of statuses
from enum import Enum, auto

class Error(Enum):
    # No error
    NONE = auto()
    
    # Invalid packets
    INVALID_HEADER_ERROR = auto()
    INVALID_ARGUMENT_ERROR = auto()

    #Accessing stuff
    KEY_ERROR = auto()

    # Valve and sensor request errors
    REQUEST_ERROR = auto()

    TELEM_CONNECTION_ERROR = auto()