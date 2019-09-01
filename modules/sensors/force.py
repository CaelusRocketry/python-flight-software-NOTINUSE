import yaml
import time
from . import Sensor, SensorStatus, SensorType
import RPI.GPIO as GPIO
# Local Imports

class Force(Sensor):

    def __init__(self, sck, dat, location):
        self.sck = sck
        self.dat = dat
        self._name = "Load Cell"
        self._location = location
        self._status = SensorStatus.Safe
        self._sensor_type = SensorType.Force
        self.data = {}
        self.timestamp = None #Indication of when last data was calculated

        with open("boundaries.yaml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        assert location in cfg['load']
        self.boundaries = {}
        self.boundaries[SensorStatus.Safe] = cfg['load'][location]['safe']
        self.boundaries[SensorStatus.Warn] = cfg['load'][location]['warn']
        self.boundaries[SensorStatus.Crit] = cfg['load'][location]['crit']

    def setup():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sck, GPIO.OUT)

    def read_weight(self):
        i = 0
        count = 0
        GPIO.setup(self.dat, GPIO.OUT)
        GPIO.output(self.dat,1)
        GPIO.output(self.sck,0)
        GPIO.setup(self.dat, GPIO.IN)

        while GPIO.input(self.dat) == 1: i = 0

        for i in range(24):
            GPIO.output(self.sck, 1)
            count = count << 1

            GPIO.output(self.sck,0)
            time.sleep(0.001)
            if GPIO.input(self.dat) == 0: #HX711 values are in 2s complement
                count = count + 1

        GPIO.output(self.sck,1)
        count = count ^ 0x800000 #clear 24th bit
        GPIO.output(self.sck,0)

        #Calibration
        weight = (958400 - count) / 845165
        return weight

    def get_data(self):
        data = {}
        data["weight"] = self.read_weight()
        data["timestamp"] = time.time()
        self.timestamp = time.time()
        self.data = data
        return data

    #This method should be constantly running in a thread, and should be the only thing calling get_data
    def check(self):
        while True:
            data = self.get_data()
            if data["weight"] >= self.boundaries[SensorStatus.Safe][0] and data["weight"] <= self.boundaries[SensorStatus.Safe][1]:
                self._status = SensorStatus.Safe
            elif data["weight"] >= self.boundaries[SensorStatus.Warn][0] and data["weight"] <= self.boundaries[SensorStatus.Warn][1]:
                self._status = SensorStatus.Warn
            else:
                self._status = SensorStatus.Crit


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
