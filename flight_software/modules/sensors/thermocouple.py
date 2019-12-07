import os
import yaml
import time
import Adafruit_GPIO
import sys
# Local Imports
from . import Sensor, SensorStatus, SensorType

try:
# if REAL:
    from Adafruit_MAX31856 import MAX31856 as MAX31856
except Exception as e:
    print(e)
    print("Skipping thermocouple on non-pi...")
    REAL = False
else:
    print("Loaded thermocouple")
    REAL = True

class PsuedoThermocouple():

    def read_internal_temp_c(self):
        return 1

    def read_temp_c(self):
        return 2

class Thermocouple(Sensor):

    def __init__(self, port, device, location):
        """
        Initializes attributes needed for thermocouple sensor class
        :param port: SPi serial port
        :param device: Which device is being communicated with
        :param location: Where temperature is being taken
        """
        self.spi_port = port
        self.spi_device = device
        self.sensor = MAX31856(hardware_spi=Adafruit_GPIO.SPI.SpiDev(port, device), tc_type=MAX31856.MAX31856_K_TYPE) \
            if REAL else PsuedoThermocouple()

        self.datatypes = ["temperature"]
        super(Thermocouple, self).__init__("thermocouple", SensorType.Thermocouple, location, self.datatypes)

    def internal(self):
        return self.sensor.read_internal_temp_c()

    def temp(self):
        return self.sensor.read_temp_c()

    def get_data(self):
        """ :return: Set of internal temperature, external temperature, and timestamp"""
        data = {}
        data["internal"] = self.internal()
        data["temperature"] = self.temp()
        data["timestamp"] = time.time()
        self.timestamp = time.time()
        self.data = data
        return data

    def check(self):
        """
        Constantly runs in the thread, calling get_data which is checked to set
        status to safe, warning, or critical

        This method should be constantly running in a thread, and should be the
        only thing calling get_data
        """
        while True:
            data = self.get_data()
            if data["temperature"] >= self.boundaries["temperature"][SensorStatus.Safe][0] and data["temperature"] <= self.boundaries["temperature"][SensorStatus.Safe][1]:
                self._status = SensorStatus.Safe
            elif data["temperature"] >= self.boundaries["temperature"][SensorStatus.Warn][0] and data["temperature"] <= self.boundaries["temperature"][SensorStatus.Warn][1]:
                self._status = SensorStatus.Warn
            else:
                self._status = SensorStatus.Crit
