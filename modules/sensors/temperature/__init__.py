from typing import List

import Adafruit_GPIO.SPI as SPI
from typing import Tuple
from queue import PriorityQueue

from modules.sensors import Sensor, SensorType, SensorStatus
from modules.sensors.temperature.max31856 import MAX31856

# Define custom types
TemperatureLevels = Tuple[float, float]


class Temperature(Sensor):
    def __init__(self, location: str, levels: TemperatureLevels):
        self.location = location
        self.levels = levels
        self.sensor = MAX31856(
            hardware_spi=SPI.SpiDev(
                0, 0), tc_type=MAX31856.MAX31856_K_TYPE)
        self.log = PriorityQueue()

    def temp(self) -> float:
        return self.sensor.read_temp_c()

    @classmethod
    def name(cls) -> str:
        return "TEMP.{}".format(cls.location()).upper()

    @classmethod
    def location(cls) -> str:
        return str(cls.location)

    @classmethod
    def status(cls) -> SensorStatus:
        pass

    @classmethod
    def sensor_type(cls) -> SensorType:
        return SensorType.Temperature

    @classmethod
    def log(cls) -> PriorityQueue:
        pass