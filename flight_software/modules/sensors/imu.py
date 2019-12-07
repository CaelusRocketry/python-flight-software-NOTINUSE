import time
# Local Imports
from . import Sensor, SensorStatus, SensorType

# REAL = True
# if REAL:
try:
    import adafruit_bno055
    import busio
    import board
except Exception as e:
    print(e)
    print("Skipping IMU on non-pi...")
    REAL = False
else:
    print("Loaded IMU module")
    REAL = True

class PseudoIMU():

    def read_accelerometer(self):
        return (1, 1, 1)

    def read_euler(self):
        return (2, 2, 2)

    def read_gravity(self):
        return (3, 3, 3)

    def read_gyroscope(self):
        return (4, 4, 4)

    def read_linear_acceleration(self):
        return (5, 5, 5)


class IMU(Sensor):

    def __init__(self, location):
        """
        Initiates attributes needed for IMU sensor class
        :param location: Location on rocket
        """

        if REAL:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = adafruit_bno055.BNO055(i2c)
        else:
            self.sensor = PseudoIMU()

        self.datatypes = ["acceleration", "roll", "tilt"]
        super(IMU, self).__init__("imu", SensorType.IMU, location, self.datatypes)

    def get_data(self):
        """
        data = {}
        euler = self.sensor.euler
        gyro = self.sensor.gyro
        linear_acceleration = self.sensor.linear_acceleration
        if euler[0] == None or euler[2] == None:
            data["tilt"] = None
        else:
            data["tilt"] = max(abs(180 - euler[0]),
                                        abs(180 - euler[2]))
        if gyro[1] == None:
            data["roll"] = None
        else:
            data["roll"] = abs(self.sensor.gyro[1])
        if None in linear_acceleration:
            data["acceleration"] = None
        else:
            data["acceleration"] = (linear_acceleration[0] ** 2 +
                                        linear_acceleration[1] ** 2 +
                                        linear_acceleration[2] ** 2) ** 0.5
        """
        euler = self.sensor.euler
        gyro = self.sensor.gyro
        linear_acceleration = self.sensor.linear_acceleration
        self.euler = euler
        self.gyro = gyro
        self.linear_acceleration = linear_acceleration
        if euler[0] != None and euler[2] != None:
            self.data["tilt"] = max(abs(180 - euler[0]),
                                        abs(180 - euler[2]))
        if gyro[1] != None:
            self.data["roll"] = abs(self.sensor.gyro[1])
        if None not in linear_acceleration:
            self.data["acceleration"] = (linear_acceleration[0] ** 2 +
                                            linear_acceleration[1] ** 2 +
                                            linear_acceleration[2] ** 2) ** 0.5
        self.data["timestamp"] = time.time()
        self.timestamp = time.time()
        return self.data

    def check(self):
        """
        Constantly runs in a thread and calls get_data. Calcculates current tilt (pitch or yaw,
        whichever one is farther away from 0), roll (deg/sec), and acceleration. Checks data
        and changes status to safe, warning, or critical
        """
        while True:
            data = self.get_data()
            stat = SensorStatus.Safe
            for key in data:
                if data[key] == None:
                    stat = SensorStatus.Crit
                    break
                
                if data[key] >= self.boundaries[key][SensorStatus.Safe][0] and data[key] <= self.boundaries[key][SensorStatus.Safe][1]:
                    stat = min(SensorStatus.Safe, stat)
                elif data[key] >= self.boundaries[key][SensorStatus.Warn][0] and data[key] <= self.boundaries[key][SensorStatus.Warn][1]:
                    stat = min(SensorStatus.Warn, stat)
                else:
                    stat = min(SensorStatus.Crit, stat)
            
            self._status = stat

