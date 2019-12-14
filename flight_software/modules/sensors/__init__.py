# /modules/sensors
from abc import ABC, abstractmethod
from enum import Enum, IntEnum
from queue import PriorityQueue
#
# from pykalman import KalmanFilter
import numpy as np
import time
import yaml

class SensorStatus(IntEnum):
    Safe = 3
    Warn = 2
    Crit = 1


class SensorType(IntEnum):
    Thermocouple = 1
    Pressure = 2
    IMU = 3
    Force = 4

class Sensor(ABC):

    def __init__(self, name, sensortype, location, datatypes):
        self._name = name   # string
        self._location = location
        self._status = SensorStatus.Safe
        self._sensor_type = sensortype
        self.data = {}
        self.normalized = {}
        self.filters = {}
        self.timestamp = None  # Indication of when last data was calculated

        with open("boundaries.yaml", "r") as ymlfile:
            cfg = yaml.load(ymlfile)

        assert location in cfg[name] # TODO: Change from assert to error log
        self.boundaries = {}
        self.datatypes = datatypes
        for datatype in datatypes:
            self.boundaries[datatype] = {}
            self.boundaries[datatype][SensorStatus.Safe] = cfg[name][location][datatype]["safe"]
            self.boundaries[datatype][SensorStatus.Warn] = cfg[name][location][datatype]["warn"]
            self.boundaries[datatype][SensorStatus.Crit] = cfg[name][location][datatype]["crit"]
        
#        self.init_kalmans()

    def init_kalmans(self):
        """
        Creates a kalman filter for each datatype of the sensor (i.e. for imu it would be [acceleration, tilt, roll]).
        - self.kalmans is a dictionary with the datatype as the key and the kalman filter object as the value.
        - self.normalized is a tuple containing the previous (clarification: normalized, previous normalized, or read?) value and covariance calculated by the kalman filter -> (normalized value, covariance).
        - @returns self.kalmans
        """

        self.kalmans = {}

        print("Creating kalman filter for ", self.name)
        print("Gathering training data")

        # Gets data from each datatype of the sensor (i.e. for imu it would be [acceleration, tilt, roll])
        training = {datatype: [] for datatype in self.datatypes}
        for i in range(10):
            current_data = self.get_data()
            for datatype in self.datatypes:
#                if current_data[datatype] != None:
                if datatype in current_data:
                    training[datatype].append(current_data[datatype])
                else:
                    print("Rip", datatype, "is None")
            time.sleep(.5)
        training = {i:np.array(training[i]) for i in training}

        # Trains each of the kalman filters with its respective training data
        for datatype in self.datatypes:
            kalman, x_now, p_now = self.create_kalman(training[datatype], 150)
            self.kalmans[datatype] = kalman
            self.normalized[datatype] = (x_now, p_now)
            print(datatype, "kalman initialized")

        print("Testing kalmans for ", self.name)
        print("Reading\t\tExpected Readings")

        # Tests each of the kalman filters with its respective data
        #readings = {datatype: np.array([]) for datatype in self.datatypes}
        for i in range(50):
            current_data = self.get_data()
            print("datatype:", datatype)
            for datatype in self.datatypes:
#                if current_data[datatype] != None:
                if datatype in current_data:
                    reading = current_data[datatype]
                    self.normalized[datatype] = self.update_kalman(datatype, reading)
                    print(datatype, "\t\t", reading, "\t\t" , self.normalized[datatype][0])
                else:
                    print("Rip", datatype, "is None")
            time.sleep(.5)
            
        return self.kalmans

    @staticmethod
    def create_kalman(training, normalizingFactor): 
        """
        Initializes the kalman filter for the sensor class and trains it using the given training data.
        - @param training: the training data -> list
        - @param normalizingFactor -> how smooth the curve will be
        """

        # Basic setup for kalman filter variables.
        training = np.asarray(training)
        print("Training", training, type(training))
        initial_state_mean = [training[0], 0] 
        transition_matrix = [[1, 1], [0, 1]]
        observation_matrix = [[1, 0]]

        # Creates a preliminary kalman filter which is used to find an optimal observation_covariance
        # think of it like using a basic neural network to find an optimal learning rate in ML
        kf_prelim = KalmanFilter(transition_matrices = transition_matrix,
                                 observation_matrices = observation_matrix,
                                 initial_state_mean = initial_state_mean)
        kf_prelim = kf_prelim.em(training, n_iter=5)
        # (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(training)

        # Creates the actual kalman filter model with the observation covariance from the first one
        kf = KalmanFilter(transition_matrices = transition_matrix,
                          observation_matrices = observation_matrix,
                          initial_state_mean = initial_state_mean,
                          observation_covariance = normalizingFactor*kf_prelim.observation_covariance,
                          em_vars=['transition_covariance', 'initial_state_covariance'])

        # Trains the actual kalman filter and finds the normalized values for the training data
        kf = kf.em(training, n_iter=5)
        (filtered_state_means, filtered_state_covariances) = kf.filter(training)
        return (kf, filtered_state_means[-1], filtered_state_covariances[-1])

    def update_kalman(self, datatype, reading):
        """
        - Updates the kalman filter based the on the current observation,
          and calculates a normalized value for the observation.
        - @param datatype: the kalman filter to use
        ####  - @param prev_res: a tuple containing the previously calculated mean and covariance valuees.
        - @param reading (number): the reading generated from the sensor.
        - x_now, P_now is the mean, covariance - where the mean is the normalized value and the covariance is the measure of spread
        - returns the normalized value
        """
        print("Updating", datatype, "kalman with reading = ", reading)
        filter = self.kalmans[datatype]
        (x_now, P_now) = self.normalized[datatype]

        # kf.filter_update is basically the predict method
        x_now, P_now = filter.filter_update(filtered_state_mean = x_now,
                                            filtered_state_covariance = P_now,
                                            observation = reading)

        self.normalized[datatype] = (x_now, P_now)
        print("New normalized value", self.normalized[datatype][0][0])

        return x_now

    @abstractmethod
    def get_data(self) -> dict:
        pass

    @abstractmethod
    def check(self) -> None:
        pass

    def name(self) -> str:
        return self._name

    def location(self) -> str:
        return self._location

    def status(self) -> SensorStatus:
        return self._status

    def sensor_type(self) -> SensorType:
        self._sensor_type

    def log(self) -> PriorityQueue:
        pass
