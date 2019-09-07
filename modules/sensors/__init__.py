from abc import ABC, abstractmethod
from enum import Enum, IntEnum
from aenum import auto
from queue import PriorityQueue

#from filterpy.kalman import KalmanFilter
#from filterpy.common import Q_discrete_white_noise
#import numpy as np


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

#    def initKalman(self):
#        self.kf = KalmanFilter( dim_x=2, dim_z=1 )
#        self.kf.x = np.array([[2.], [0.]])
#        self.kf.F = np.array([[1.,1.], [0.,1.]])
#        self.kf.H = np.array([[1.,0.]])
#        self.kf.P *= 1000.0
#        self.kf.R = 5
#        self.kf.Q = Q_discrete_white_noise(dim=2, dt=0.1, var=0.13)

#    def updateKalman(self, reading):
#        self.kf.predict()
#        self.kf.update(reading)
#        return self.kf.x


class ValveType(Enum):
    Ball = auto()
    Vent = auto()
    Drain = auto()
