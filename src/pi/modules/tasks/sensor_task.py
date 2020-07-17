from modules.tasks.task import Task
from modules.drivers.arduino import Arduino
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.lib.enums import SensorType, SensorLocation
import struct

class SensorTask(Task):
    def __init__(self, registry: Registry, flag: Flag):
        self.name = "Sensor Arduino"
        self.registry = registry
        self.flag = flag


    def begin(self, config: dict):
        self.config = config["sensors"]
        sensors = self.config["list"]
        self.sensor_list = [(s_type, loc) for s_type in sensors for loc in sensors[s_type]]
        self.num_sensors = len(self.sensor_list)
        self.arduino = Arduino(self.name, self.config)
        self.send_sensor_info()


    def send_sensor_info(self):
        byts = 
        for s_type, loc in self.sensor_list:
            #TODO: Implement this
            pass


    def get_float(self, data):
        byte_array = bytes(data)
        return struct.unpack('f', byte_array)[0]


    def read(self):
        data = self.arduino.read(self.num_sensors * 4)
        assert(len(data) == self.num_sensors * 4)

        for i in range(self.num_sensors):
            sensor_type, sensor_location = self.sensor_list[i]
            byte_value = data[i*4:(i+1)*4]
            float_value = self.get_float(byte_value)
            assert(isinstance(float_value, float))
            self.registry.put(("sensor_measured", sensor_type, sensor_location), float_value)


    def actuate(self):
        return
