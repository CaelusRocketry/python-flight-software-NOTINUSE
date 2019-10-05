from __init__ import Sensor, SensorStatus, SensorType
import numpy as np
import matplotlib.pyplot as plt


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


sensor = KalmanTestSensor("nowhere")
training = np.array([399, 403, 409, 416])
readings = [418, 420, 429, 423, 429, 431, 433, 434, 434, 433, 431, 430, 428, 427, 425, 429, 431, 410, 406, 402, 397, 391, 376, 372, 351, 336, 327, 307]
    
sensor.initKalman(training, 150)

expected_readings = sensor.updateKalman(readings)

readings = np.asarray(readings)


plt.figure(3)
times = range(readings.shape[0])
old_times = range(training.shape[0])
new_times = range(readings.shape[0])

plt.plot(times, readings, 'bo')
plt.plot(new_times, expected_readings[:, 0], 'go')
plt.plot(new_times, expected_readings[:, 0], 'g--')
plt.plot(new_times, readings, 'yo')

plt.show()










