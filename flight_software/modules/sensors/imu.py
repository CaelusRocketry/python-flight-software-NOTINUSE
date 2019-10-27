import yaml
import time
# Local Imports
from . import Sensor, SensorStatus, SensorType

# REAL = True
# if REAL:
try:
    import adafruit_bno055
    import busio
    import board
except:
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
        self._name = "IMU"
        self._location = location
        self._status = SensorStatus.Safe
        self._sensor_type = SensorType.IMU
        self.data = {}
        self.timestamp = None  # Indication of when last data was calculated

        with open("boundaries.yaml" if REAL else "flight_software/boundaries.yaml", "r") as ymlfile:
            cfg = yaml.load(ymlfile)
        assert location in cfg["imu"]
        self.boundaries = {}
        for datatype in ["acceleration", "roll", "tilt"]:
            self.boundaries[datatype] = {}
            self.boundaries[datatype][SensorStatus.Safe] = cfg["imu"][location][datatype]["safe"]
            self.boundaries[datatype][SensorStatus.Warn] = cfg["imu"][location][datatype]["warn"]
            self.boundaries[datatype][SensorStatus.Crit] = cfg["imu"][location][datatype]["crit"]

    def get_data(self):
        data = {}
        data["accleration"] = self.sensor.accelerometer
        data["euler"] = self.sensor.euler
        data["gravity"] = self.sensor.gravity
        data["gyroscope"] = self.sensor.gyroscope
        data["linear_acceleration"] = self.sensor.linear_acceleration
        data["timestamp"] = time.time()
        self.timestamp = time.time()
        self.data = data
        return data

    def check(self):
        """
        Constantly runs in a thread and calls get_data. Calcculates current tile (pitch or yaw,
        whichever one is farther away from 0), roll (deg/sec), and acceleration. Checks data
        and changes status to safe, warning, or critical
        """
        while True:
            data = self.get_data()
            check_data = {}
            check_data["tilt"] = max(abs(180 - data["euler"][0]),
                                     abs(180 - data["euler"][2]))
            check_data["roll"] = abs(data["gyroscope"][1])
            check_data["acceleration"] = (data["linear_acceleration"][0] ** 2 +
                                          data["linear_acceleration"][1] ** 2 +
                                          data["linear_acceleration"][2] ** 2) ** 0.5
            stat = SensorStatus.Safe
            for key in check_data:
                if check_data[key] >= self.boundaries[key][SensorStatus.Safe][
                        0] and check_data[key] <= self.boundaries[key][SensorStatus.Safe][1]:
                    stat = min(SensorStatus.Safe, stat)
                elif check_data[key] >= self.boundaries[key][SensorStatus.Warn][0] and check_data[key] <= self.boundaries[key][SensorStatus.Warn][1]:
                    stat = min(SensorStatus.Warn, stat)
                else:
                    stat = min(SensorStatus.Crit, stat)
            self._status = stat

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
