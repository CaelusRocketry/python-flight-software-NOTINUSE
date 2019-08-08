from abc import ABC
from enum import Enum, auto


class SensorStatus(Enum):
    Safe = auto()
    Warn = auto()
    Crit = auto()


class SensorType(Enum):
    Temperature = auto()
    Pressure = auto()
    IMU = auto()
    Force = auto()


class Sensor(ABC):
    pass
