from modules.tasks.task import Task
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.lib.enums import SensorType, SensorLocation
import struct
import time

SEND_DATA_CMD = 255
CONFIRMATION = 255
#f = open("black_box_coldflow.txt", "w+")
class SensorTask(Task):
    def __init__(self, registry: Registry, flag: Flag):
        self.name = "sensor_arduino"
        self.registry = registry
        self.flag = flag


    def begin(self, config: dict):
        #TODO: fix this, it's really hacky and just a temporary workaround (let's see how long it stays though)
        self.config = config["sensors"]
        self.sensor_config = self.config["list"]
        self.sensor_list = [(s_type, loc) for s_type in self.sensor_config for loc in self.sensor_config[s_type]]
        self.num_sensors = len(self.sensor_list)
        if config["arduino_type"] == "pseudo":
            from modules.drivers.pseudo_arduino import Arduino
            self.arduino = Arduino(self.name, self.config, self.registry)
        else:
            from modules.drivers.real_arduino import Arduino
            self.arduino = Arduino(self.name, self.config)
        self.send_sensor_info()
        print("sensor initialized!!!!!")

    def send_sensor_info(self):
        self.pins = {}
        num_pressures = len(self.sensor_config[SensorType.PRESSURE])
        num_thermos = len(self.sensor_config[SensorType.THERMOCOUPLE])
        to_send = [len(self.sensor_list), num_thermos, num_pressures]
        for s_type, loc in self.sensor_list:
            if s_type == SensorType.PRESSURE:
                to_send.append(1)
                pin = self.sensor_config[s_type][loc]["pin"]
                to_send.append(pin)
                self.pins[pin] = (s_type, loc)
            elif s_type == SensorType.THERMOCOUPLE:
                to_send.append(0)
                pins = self.sensor_config[s_type][loc]["pins"]
                for pin in pins:
                    to_send.append(pin)
                self.pins[pins[0]] = (s_type, loc)
            else:
                raise Exception("Unknown sensor type")
        self.arduino.write(bytes(to_send))
        var = self.arduino.read(1) 
#        print("HI", var)
 #       print("sensor data is being sent")
        # assert(var == bytes([CONFIRMATION]))


    def get_float(self, data):
        byte_array = bytes(data)
        return struct.unpack('f', byte_array)[0]


    def read(self):
        # print(self.pins)
        self.arduino.write([SEND_DATA_CMD])
        data = self.arduino.read(self.num_sensors * 5)
        assert(len(data) == self.num_sensors * 5)
 #       print("data")
        for i in range(self.num_sensors):
            temp = data[i*5: (i + 1)*5] # Isolate the block of data for that sensor
  #          print(temp)
            pin = temp[0]
            assert(pin in self.pins)
            sensor_type, sensor_location = self.pins[pin]
            byte_value = temp[1:]
            float_value = self.get_float(byte_value)
            assert(isinstance(float_value, float))
            self.registry.put(("sensor_measured", sensor_type, sensor_location), float_value)
  #          print("ya i am reading data")
            f = open("black_box_coldflow.txt", "a+")
   #         print("data is being logged into the file")
            f.write(str(time.time()) + " ")
            f.write(str(sensor_type) + " " + str(sensor_location) + " " + str(float_value) + "\n")
            print(str(sensor_location)+" "+ str(float_value), end=" ")
            f.close()
        print()

    def actuate(self):
        return
