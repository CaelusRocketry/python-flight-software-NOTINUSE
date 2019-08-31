from abc import ABC, abstractmethod
from enum import IntEnum, Enum
from aenum import auto
from queue import PriorityQueue

class SensorStatus(IntEnum):
    Safe = 3
    Warn = 2
    Crit = 1

class SensorType(Enum):
    Temperature = auto()
    Pressure = auto()
    IMU = auto()
    Force = auto()

class Sensor(ABC):
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def location(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def status(cls) -> SensorStatus:
        pass

    @classmethod
    @abstractmethod
    def sensor_type(cls) -> SensorType:
        pass

    @classmethod
    @abstractmethod
    def log(cls) -> PriorityQueue:
        pass
