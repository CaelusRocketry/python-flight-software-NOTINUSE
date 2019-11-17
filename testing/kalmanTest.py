import sys
import os
sys.path.append("../flight_software/modules/")
os.chdir("../flight_software")
from sensors import Sensor, SensorStatus, SensorType
from sensors.imu import IMU
# from force import Load
import numpy as np
import matplotlib.pyplot as plt
import time

imu = IMU("nose")

readings = []
kalman_output  = []
for i in range(50):
    current_data = imu.get_data()
    readings.append(current_data["tilt"])
    kalman_output.append(imu.updateKalman("tilt", current_data["tilt"])[0][0])
    print("Changed values:", readings[-1], kalman_output[-1])
    time.sleep(.5)

readings = np.array(readings)
kalman_output = np.array(kalman_output)
print(kalman_output)


plt.figure(3)	
times = range(readings.shape[0])	
new_times = range(readings.shape[0])	


plt.plot(times, readings, 'bo')	
plt.plot(new_times, kalman_output[:, 0], 'go')	
plt.plot(new_times, kalman_output[:, 0], 'g--')	
plt.plot(new_times, readings, 'yo')	


plt.show()
print("Plot should be showing")