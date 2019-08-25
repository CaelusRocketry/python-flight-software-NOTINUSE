import yaml
import time
import Adafruit_GPIO
# Local Imports
from Adafruit_MAX31856 import MAX31856 as MAX31856

class Thermocouple(Sensor):
    
    def __init__(self, location):
        SPI_PORT = 0
        SPI_DEVICE = 0
        self.sensor = MAX31856(hardware_spi=Adafruit_GPIO.SPI.SpiDev(SPI_PORT, SPI_DEVICE), tc_type=MAX31856.MAX31856_K_TYPE)
        self.name = "Thermocouple"
        self.location = location
        self.status = SensorStatus.Safe
        self.sensor_type = SensorType.Temperature
        self.data = {}
        self.timestamp = None #Indication of when last data was calculated
        
        with open("boundaries.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        assert location in cfg['thermocouple']
        self.boundaries = {}
        self.boundaries[SensorStatus.Safe] = cfg['thermocouple'][location]['safe']
        self.boundaries[SensorStatus.Warn] = cfg['thermocouple'][location]['warn']
        self.boundaries[SensorStatus.Crit] = cfg['thermocouple'][location]['crit']
        
    def internal(self):
        return sensor.read_internal_temp_c()

    def temp(self):
        return sensor.read_temp_c()
    
    def get_data(self):
        data = {}
        data["internal"] = self.internal()
        data["temp"] = self.temp()
        self.data = data
        self.timestamp = time.time()
        return data
    
    #This method should be constantly running in a thread, and should be the only thing calling get_data
    def check(self):
        while True:
            data = self.get_data()
            if data["temp"] >= self.boundaries[SensorStatus.Safe][0] and data["temp"] <= self.boundaries[SensorStatus.Safe][1]:
                self.status = SensorStatus.Safe
            elif data["temp"] >= self.boundaries[SensorStatus.Warn][0] and data["temp"] <= self.boundaries[SensorStatus.Warn][1]:
                self.status = SensorStatus.Warn
            else:
                self.status = SensorStatus.Crit

    def name(self):
        return self.name
    
    def location(self):
        return self.location
    
    def status(self):
        return self.status
    
    def sensor_type(self):
        return self.sensor_type
    
    def log(self):
        pass