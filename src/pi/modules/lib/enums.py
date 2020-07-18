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


class SolenoidState(IntEnum):
    OPEN = 1
    CLOSED = 0


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


class ActuationType(IntEnum):
    PULSE = 4
    OPEN_VENT = 3
    CLOSE_VENT = 2
    NONE = 1


class ValvePriority(IntEnum):
    NONE = 0
    LOW_PRIORITY = 1
    PI_PRIORITY = 2
    MAX_TELEMETRY_PRIORITY = 3
    ABORT_PRIORITY = 4


class Stage(str, Enum):
    PROPELLANT_LOADING = "propellant_loading"
    LEAK_TESTING_1 = "leak_testing_1"
    PRESSURANT_LOADING = "pressurant_loading"
    LEAK_TESTING_2 = "leak_testing_2"
    PRE_IGNITION = "pre_ignition"
    DISCONNECTION = "disconnection"
