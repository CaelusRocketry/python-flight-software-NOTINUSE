import time

# https://learn.adafruit.com/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black/overview
try:
    from Adafruit_BNO055 import BNO055
    IMU = BNO055.BNO055()
    IMU.begin()

except ImportError:
    import random

    class IMU:

        def __init__(self):
            pass

        def read_euler():
            return (random.random()*360, random.random()*360, random.random()*360)

    IMU = IMU()

def test():
    while True:
        print("ACC", IMU.read_accelerometer())
        print("EULER", IMU.read_euler())
        print("GRAV", IMU.read_gravity())
        print("GRYO", IMU.read_gyroscope())
        print("LINACC", IMU.read_linear_acceleration())
        # print(IMU.read_quaternion())
        time.sleep(0.5)
