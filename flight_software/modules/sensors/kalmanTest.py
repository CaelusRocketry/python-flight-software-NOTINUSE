from __init__ import Sensor, SensorStatus, SensorType
from imu import IMU
from force import Load
from thermocouple import Thermocouple
import numpy as np
import matplotlib.pyplot as plt
import time


class KalmanTestSensor(Sensor):

    def __init__(self, location):
        print(location)

    def name(self):
        return self._name

    def location(self):
        return self._location

    def status(self):
        return self._status

    def sensor_type(self):
        return self._sensor_type

    def log(self):
        pass

# Testing IMU data normalizing
imu = IMU("IMU")

print("Gathering test data")

training = np.array([])
for i in range(10):
    training.append(imu.get_data()["gyroscope"])
    time.sleep(500)

imu.initKalman(training, 150)

print("Gathering Data")

readings = np.array([])
for i in range(50):
    readings.append(imu.get_data()["gyroscope"])

expected_readings = imu.updateKalman(readings)

print("Reading\t\tExpected Readings")
for i in range(len(readings)):
    print(readings[i] + "\t\t" + expected_readings[i])

# Testing force
force = Load("force")

print("Gathering test data")

training = np.array([])
for i in range(10):
    training.append(force.get_data()["weight"])
    time.sleep(500)

force.initKalman(training, 150)

print("Gathering Data")

readings = np.array([])
for i in range(50):
    readings.append(force.get_data()["weight"])

expected_readings = force.updateKalman(readings)

print("Reading\t\tExpected Readings")
for i in range(len(readings)):
    print(readings[i] + "\t\t" + expected_readings[i])

# Testing thermocouple

thermocouple = Thermocouple("Thermocouple")

print("Gathering test data")

training = np.array([])
for i in range(10):
    training.append(thermocouple.get_data()["temp"])
    time.sleep(500)

thermocouple.initKalman(training, 150)

print("Gathering Data")

readings = np.array([])
for i in range(50):
    readings.append(thermocouple.get_data()["temp"])

expected_readings = thermocouple.updateKalman(readings)

print("Reading\t\tExpected Readings")
for i in range(len(readings)):
    print(readings[i] + "\t\t" + expected_readings[i])