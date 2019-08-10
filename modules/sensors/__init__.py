from abc import ABC, abstractmethod
from enum import Enum, auto
from queue import PriorityQueue


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
