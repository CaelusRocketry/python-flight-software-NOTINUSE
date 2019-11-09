# /modules/sensors

from abc import ABC, abstractmethod
from enum import Enum, IntEnum
from queue import PriorityQueue
import yaml

# from . import force, imu, thermocouple

class SensorStatus(IntEnum):
    Safe = 3
    Warn = 2
    Crit = 1


class SensorType(IntEnum):
    Temperature = 1
    Pressure = 2
    IMU = 3
    Force = 4


class Sensor(ABC):

    def __init__(self, name, sensortype, location):
        self._name = name
        self._location = location
        self._status = SensorStatus.Safe
        self._sensor_type = sensortype
        self.data = {}
        self.normalized = {}
        self.filters = {}
        self.timestamp = None  # Indication of when last data was calculated

        with open("boundaries.yaml", "r") as ymlfile:
            cfg = yaml.load(ymlfile)
        assert location in cfg[self.sensor_type]
        self.boundaries = {}
        for datatype in ["acceleration", "roll", "tilt"]:
            self.boundaries[datatype] = {}
            self.boundaries[datatype][SensorStatus.Safe] = cfg[name][location][datatype]["safe"]
            self.boundaries[datatype][SensorStatus.Warn] = cfg[name][location][datatype]["warn"]
            self.boundaries[datatype][SensorStatus.Crit] = cfg[name][location][datatype]["crit"]



    @classmethod
    def name(cls) -> str:
        return self._name

    @classmethod
    def location(cls) -> str:
        return self._location

    @classmethod
    def status(cls) -> SensorStatus:
        return self._status

    @classmethod
    def sensor_type(cls) -> SensorType:
        self._sensor_type

    @classmethod
    @abstractmethod
    def log(cls) -> PriorityQueue:
        pass


from . import force, imu, thermocouple
