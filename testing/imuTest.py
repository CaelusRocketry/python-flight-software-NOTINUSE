import time
import sys
import os
sys.path.append("../flight_software/modules/")
os.chdir("../flight_software")
from sensors.imu import IMU

imu = IMU("nose")
for i in range(50):
#    data = imu.get_data()
#    if "tilt" in data:
#        print("tilt:", data["tilt"])
#    if "roll" in data:
#        print("roll:", data["roll"])
    imu.get_data()
    print("Euler:", imu.euler)
    print("Gyro:", imu.gyro)
    print("Acceleration:", imu.linear_acceleration)
    time.sleep(0.5)