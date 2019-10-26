# /modules/sensors

from abc import ABC, abstractmethod
from enum import Enum, IntEnum
from queue import PriorityQueue

from pykalman import KalmanFilter
import numpy as np

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

    def initKalman(self, training, normalizingFactor): 
        training = np.asarray(training)
        initial_state_mean = [training[0], 0] 
        transition_matrix = [[1, 1], [0, 1]]
        observation_matrix = [[1, 0]]

        kf1 = KalmanFilter(transition_matrices = transition_matrix,
                observation_matrices = observation_matrix,
                initial_state_mean = initial_state_mean)
        kf1 = kf1.em(training, n_iter=5)
        # (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(training)

        self.kf = KalmanFilter(transition_matrices = transition_matrix,
                        observation_matrices = observation_matrix,
                        initial_state_mean = initial_state_mean,
                        observation_covariance = normalizingFactor*kf1.observation_covariance,
                        em_vars=['transition_covariance', 'initial_state_covariance'])

        self.kf = self.kf.em(training, n_iter=5)
        (self.filtered_state_means, self.filtered_state_covariances) = self.kf.filter(training)                

    def updateKalman(self, readings):
        readings = np.asarray(readings)
        x_now = self.filtered_state_means[-1]
        P_now = self.filtered_state_covariances[-1]
        x_new = np.zeros((len(readings), self.filtered_state_means.shape[1]))


        # For each new measurement (this is the live update loop)
        for i, reading in enumerate(readings):
            # kf.filter_update is basically the predict method
            (x_now, P_now) = self.kf.filter_update(filtered_state_mean = x_now,
                                                filtered_state_covariance = P_now,
                                                observation = reading)
            # x_now is the normalized data point
            x_new[i] = x_now
        
        return x_new

        


