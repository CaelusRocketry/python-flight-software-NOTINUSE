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
        self.sensor_config = self.config["list"]
        self.sensor_list = [(s_type, loc) for s_type in self.sensor_config for loc in self.sensor_config[s_type]]
        self.num_sensors = len(self.sensor_list)
        self.arduino = Arduino(self.name, self.config)
        self.send_sensor_info()


    def send_sensor_info(self):
        self.pins = {}
        to_send = [len(self.sensor_list)]
        for s_type, loc in self.sensor_list:
            if s_type == SensorType.PRESSURE:
                to_send.append(1)
                pin = self.sensor_config[s_type][loc]["pin"]
                to_send.append(pin)
                self.pins[pin] = (s_type, loc)
            elif s_type == SensorType.THERMOCOUPLE:
                to_send.append(0)
                pins = self.sensor_config[s_type][loc]["pin"]
                for pin in pins:
                    to_send.append(pin)
                self.pins[pins[0]] = (s_type, loc)
            else:
                raise Exception("Unknown sensor type")
        self.arduino.write(to_send)


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
