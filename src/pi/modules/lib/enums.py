import json
from enum import Enum, IntEnum, auto

class SensorType(str, Enum):
    THERMOCOUPLE = "thermocouple"
    PRESSURE = "pressure"
    LOAD = "load"


class SensorLocation(str, Enum):
    PT1 = "PT-1"
    PT2 = "PT-2"


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
    PRESSURIZATION = "pressurization"
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
    WAITING = "waiting"
    PRESSURIZATION = "pressurization"
    AUTOSEQUENCE = "autosequence"
    POSTBURN = "postburn"
