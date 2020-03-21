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


    def begin(self, config: dict):
        self.config = config["sensors"]
        #TODO: Make sure that this is the same order that the arduino returns its data in
        sensors = self.config["list"]
        self.sensor_list = [(s_type, loc) for s_type in sensors for loc in sensors[s_type]]
        self.num_sensors = len(self.sensor_list)
        self.arduino = Arduino(self.name, self.config)


    def get_float(self, data):
        byte_array = bytes(data)
        return struct.unpack('f', byte_array)[0]


    def read(self) -> Error:
        data = self.arduino.read(self.num_sensors * 4)
        assert(len(data) == self.num_sensors * 4)

        for i in range(self.num_sensors):
            sensor_type, sensor_location = self.sensor_list[i]
            byte_value = data[i*4:(i+1)*4]
            float_value = self.get_float(byte_value)
            assert(isinstance(float_value, float))
            self.registry.put(("sensor", sensor_type, sensor_location), float_value)

    
    def actuate(self):
        return
