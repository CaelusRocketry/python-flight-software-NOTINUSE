import random
import struct
from .driver import Driver
"""
Pseudo arduino class to use to run code on ur own laptop!
FIXME: The real_arduino.py class should be used on the pi!
"""
class PseudoSensor():
    def __init__(self):
        self.sensors = {"thermo1": 0, "thermo2": 0, "pressure1": 0, "pressure2": 0, "pressure3": 0, "load": 0}


    def set_sensor_values(self):
        self.sensors = {i: random.random() * 50 for i in self.sensors}


    def read(self):
        self.set_sensor_values()
        ret = bytes()
        for key in self.sensors:
            ret += struct.pack('f', self.sensors[key])
        return ret
    
    def write(self, msg):
        pass


class PseudoValve():
    def __init__(self, config: dict):
        self.config = config
        sensors = config["list"]
        self.sensor_list = [(s_type, loc) for s_type in sensors for loc in sensors[s_type]]
        self.num_sensors = len(self.sensor_list)


    def set_sensor_values(self):
        self.sensors = {i: random.random() * 50 for i in self.sensor_list}


    def read(self):
        self.set_sensor_values()
        ret = bytes()
        for key in self.sensors:
            ret += struct.pack('f', self.sensors[key])
        return ret
    
    def write(self, msg):
        pass


class Arduino(Driver):

    def __init__(self, name: "str", config: dict):
        super().__init__(name)
        self.name = name
        self.config = config
        self.address = self.config["address"]
        self.reset()
    
    """
    Return whether or not the i2c connection is alive
    """
    def status(self) -> bool:
        # ping = "hey u alive"
        # ping_bytes = [ord(b) for b in ping]
        # self.write(ping_bytes)

        # time.sleep(.3)

        # response = self.read()
        # return struct.unpack('f', response)[0] == "yeah i'm good"
        pass

    """
    Powercycle the arduino
    """
    def reset(self) -> bool:
        if self.name == "Sensor Arduino":
            self.arduino = PseudoSensor(self.config)
        else:
            self.arduino = PseudoValve(self.config)

    """
    Read data from the Arduino and return it
    Ex. [10, 20, 0, 0, 15, 0, 0, 0, 14, 12, 74, 129]
    """
    def read(self, num_bytes: int) -> bytes:
        return self.arduino.read()

    """
    Write data to the Arduino and return True if the write was successful else False
    """
    def write(self, msg: bytes) -> bool:
        self.arduino.write(msg)
    