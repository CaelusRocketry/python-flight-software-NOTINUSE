# Enumeration of statuses
from enum import Enum, auto

class AccessError(Enum):
    KEY_ERROR = auto()
    TYPE_ERROR = auto()
    NONE = None

class ValveActuationError(Enum):
    VALVE_TYPE_ERROR = auto()    
    LOCATION_ERROR = auto()
    ACTUATION_TYPE_ERROR = auto()
    ACTUATION_VALUE_ERROR = auto()

class SensorRequestError(Enum):
    SENSOR_TYPE_ERROR = auto()
    SENSOR_LOCATION_ERROR = auto()

class ValveRequestError(Enum):
    VALVE_TYPE_ERROR = auto()
    VALVE_LOCATION_ERROR = auto()

class PacketError(Enum):
    INVALID_HEADER_ERROR = auto()

