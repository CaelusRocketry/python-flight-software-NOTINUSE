import yaml
import time
try:
    import RPi.GPIO as GPIO
except: 
    print("Skipping GPIO on non-pi...")
    REAL = False
else:
    print("Loaded GPIO")
    REAL = True
# Local Imports
from . import Sensor, SensorStatus, SensorType

class Load(Sensor):

    def __init__(self, sck, dat, location):
        """ Initiates attributes needed for Load sensor class
            :param sck: Serial clock
            :param dat: Data pin number
            :param location: Location on rocket"""
        self.sck = sck
        self.dat = dat

        self.datatypes = ["weight"]
        super(Load, self).__init__("load", SensorType.Force, location, self.datatypes)
        self.setup()

    def setup(self):
        if REAL:
             GPIO.setwarnings(False)
             GPIO.setmode(GPIO.BCM)
             GPIO.setup(self.sck, GPIO.OUT)

    def read_weight(self):
        i = 0
        count = 0
        GPIO.setup(self.dat, GPIO.OUT)
        GPIO.output(self.dat, 1)
        GPIO.output(self.sck, 0)
        GPIO.setup(self.dat, GPIO.IN)

        while GPIO.input(self.dat) == 1:
            i = 0

        # Calculates the kg value of the load cell using the clock and reading from the data pin
        for i in range(24):
            GPIO.output(self.sck, 1)
            count = count << 1

            GPIO.output(self.sck, 0)
            time.sleep(0.001)
            if GPIO.input(self.dat) == 0:  # HX711 values are in 2s complement
                count = count + 1

        GPIO.output(self.sck, 1)
        count = count ^ 0x800000  # clear 24th bit
        GPIO.output(self.sck, 0)

        # Calibration
        weight = (9584000 - count) / 845165
        return weight

    def get_data(self):
        data = {}
        data["weight"] = self.read_weight()
        data["timestamp"] = time.time()
        self.timestamp = time.time()
        self.data = data
        return data

    def check(self):
        """
        Constantly runs in the thread, calling get_data which is checked to set
        status to safe, warning, or critical.

        This method should be constantly running in a thread, and should be the
        only thing calling get_data
        """
        while True:
            data = self.get_data()
            if data["weight"] >= self.boundaries[SensorStatus.Safe][0] and data["weight"] <= self.boundaries[SensorStatus.Safe][1]:
                self._status = SensorStatus.Safe
            elif data["weight"] >= self.boundaries[SensorStatus.Warn][0] and data["weight"] <= self.boundaries[SensorStatus.Warn][1]:
                self._status = SensorStatus.Warn
            else:
                self._status = SensorStatus.Crit
