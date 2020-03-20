import json
from enum import Enum, IntEnum, auto

class SensorType(str, Enum):
    THERMOCOUPLE = "thermocouple"
    PRESSURE = "pressure"
    LOAD = "load"


class SensorLocation(str, Enum):
    CHAMBER = "chamber"
    TANK = "tank"
    INJECTOR = "injector"


class SolenoidState(str, Enum):
    OPEN = 'open'
    CLOSED = "closed"


class SensorStatus(IntEnum):
    SAFE = 3
    WARNING = 2
    CRITICAL = 1


class ValveType(str, Enum):
    SOLENOID = "solenoid"
    BALL = "ball"


class ValveLocation(str, Enum):
    PRESSURE_RELIEF = "pressure_relief"
    PROPELLANT_VENT = "propellant_vent"
    MAIN_PROPELLANT_VALVE = "main_propellant_valve"


class ActuationType(str, Enum):
    PULSE = "pulse"
    OPEN_VENT = "open_vent"
    CLOSE_VENT = "close_vent"
    NONE = None


class Stage(IntEnum):
    PROPELLANT_LOADING = 1
    LEAK_TESTING_1 = 2
    PRESSURANT_LOADING = 3
    LEAK_TESTING_2 = 4
    PRE_IGNITION = 5
    DISCONNECTION = 6


ENUMS = [SensorType, SensorLocation, SolenoidState, ValveType, ValveLocation, ActuationType, Stage]
class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        print("TYPE: ", type(obj))
        if type(obj) in ENUMS:
            string = str(obj)
#            return string[string.index(".") + 1:]
            return string
        return json.JSONEncoder.default(self, obj)
