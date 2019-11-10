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
    Thermocouple = 1
    Pressure = 2
    IMU = 3
    Force = 4


class Sensor(ABC):

    def __init__(self, name, sensortype, location, datatypes):
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
        self.datatypes = datatypes
        for datatype in datatypes:
            self.boundaries[datatype] = {}
            self.boundaries[datatype][SensorStatus.Safe] = cfg[name][location][datatype]["safe"]
            self.boundaries[datatype][SensorStatus.Warn] = cfg[name][location][datatype]["warn"]
            self.boundaries[datatype][SensorStatus.Crit] = cfg[name][location][datatype]["crit"]
        
        self.initKalmans()

    def initKalmans(self):
        """
        Creates a kalman filter for each datatype of the sensor (i.e. for imu it would be [acceleration, tilt, roll]).
        - self.kalmans is a dictionary with the datatype as the key and the kalman filter object as the value.
        - self.normalized is a tuple containing the previous value and covariance calculated by the kalman filter -> (normalized value, covariance).
        - @returns self.kalmans
        """

        self.kalmans = {}

        print("Creating kalman filter for ", self.name)
        print("Gathering training data")

        # Gets data from each datatype of the sensor (i.e. for imu it would be [acceleration, tilt, roll])
        training = {datatype: np.array([]) for datatype in self.datatypes}
        for i in range(10):
            data = self.get_data()
            for datatype in self.datatypes:
                training[datatype].append(self.get_data()[datatype])
            time.sleep(.5)

        # Trains each of the kalman filters with its respective training data
        for datatype in self.datatypes:
            kalman, prev = self.createKalman(training, 150)
            self.kalmans[datatype] = kalman
            self.normalized[datatype] = prev

        #print("Testing kalmans for ", self.name)
        #print("Reading\t\tExpected Readings")

        # Tests each of the kalman filters with its respective data
        readings = {datatype: np.array([]) for datatype in self.datatypes}
        for i in range(50):
            data = self.get_data()
            for datatype in self.datatypes:
                reading = data[datatype]
                self.normalized[datatype] = updateKalman(self.kalmans[datatype], self.normalized[datatype], reading)
                #print(reading + "\t\t" + self.normalized[datatype][0])
            
        return self.kalmans

    @staticmethod
    def createKalman(training, normalizingFactor): 
        """
        Initializes the kalman filter for the sensor class and trains it using the given training data.
        - @param training: the training data -> list
        - @param normalizingFactor -> int: can anna or mitali explain this plz?
        """

        # Basic setup for kalman filter variables.
        training = np.asarray(training)
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
        return kf, (filtered_state_means[-1], filtered_state_covariances[-1])

    @staticmethod
    def updateKalman(filter, prev, reading):
        """
        - Updates the kalman filter based the on the current observation,
        and calculates a normalized value for the observation.
        - @param filter: the kalman filter to use
        - @param prev: a tuple containing the previously calculated mean and covariance valuees.
        - @param reading (number): the reading generated from the sensor.
        - returns (mean, covariance) where the mean is the normalized value and the covariance is the 
        """

        readings = np.asarray(readings)
        (x_now, P_now) = prev

        # kf.filter_update is basically the predict method
        (x_now, P_now) = self.kf.filter_update(filtered_state_mean = x_now,
                                            filtered_state_covariance = P_now,
                                            observation = reading)
        return x_now, P_now

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
