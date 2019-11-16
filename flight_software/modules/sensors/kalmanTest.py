from __init__ import Sensor, SensorStatus, SensorType
from imu import IMU
# from force import Load
# from thermocouple import Thermocouple
import numpy as np
import matplotlib.pyplot as plt
import time

imu = IMU("test")

readings = np.array([])
kalman_output  = np.array([])
for i in range(50):
    current_data = imu.get_data()
    readings.append(current_data["gyro"])
    kalman_output.append(imu.updateKalman("gyro", current_data["gyro"]))

print(kalman_output)


plt.figure(3)	
times = range(readings.shape[0])	
new_times = range(readings.shape[0])	


plt.plot(times, readings, 'bo')	
plt.plot(new_times, kalman_output[:, 0], 'go')	
plt.plot(new_times, kalman_output[:, 0], 'g--')	
plt.plot(new_times, readings, 'yo')	


plt.show()