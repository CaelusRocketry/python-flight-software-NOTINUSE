from modules.tasks.task import Task
from modules.drivers.arduino import Arduino
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.lib.errors import Error
from modules.lib.enums import SensorType, SensorLocation
import struct

#TODO: Check w/ some boundaries file (boundaries should be part of config.json) and correspondingly update sensor statuses in registry
class SensorTask(Task):
    def __init__(self, registry: Registry, flag: Flag):
        self.name = "Sensor Arduino"
        self.registry = registry
        self.flag = flag
        #TODO: Make sure that this is the same order that the arduino returns its data in
        self.sensors = [(SensorType.THERMOCOUPLE, SensorLocation.CHAMBER),
                             (SensorType.THERMOCOUPLE, SensorLocation.TANK),
                             (SensorType.PRESSURE, SensorLocation.CHAMBER),
                             (SensorType.PRESSURE, SensorLocation.TANK),
                             (SensorType.PRESSURE, SensorLocation.INJECTOR),
                             (SensorType.LOAD, SensorLocation.TANK)]
        self.num_sensors = len(self.sensors)

    def begin(self, config):
        self.address = 0x04
        self.arduino = Arduino("Arduino Sensor", self.address)

    def get_float(self, data):
        byte_array = bytes(data)
        return struct.unpack('f', byte_array)[0]

    def read(self) -> Error:
        data = self.arduino.read(self.num_sensors * 4)
        assert(len(data) == self.num_sensors * 4)

        for i in range(self.num_sensors):
            sensor_type, sensor_location = self.sensors[i]
            byte_value = data[i*4:(i+1)*4]
            float_value = self.get_float(byte_value)
            assert(isinstance(float_value, float))
            self.registry.put(("sensor", sensor_type, sensor_location), float_value)

    
    def actuate(self):
        return
