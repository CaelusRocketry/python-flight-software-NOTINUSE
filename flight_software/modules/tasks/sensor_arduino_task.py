from modules.tasks.task import Task
from modules.drivers.arduino import Arduino
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
import struct

class SensorArduinoTask(Task):
    def __init__(self):
        self.address = 0x04
        self.name = "Arduino"
        super().__init__("Arduino", Arduino("Arduino Sensor", self.address))       # access arduino through self.driver

    def get_float(self, data, index):
        data = data[index:index+4]
        byte_array = bytes(data)
        return struct.unpack('f', byte_array)[0]

    def read(self, state_field_registry: Registry, flag: Flag) -> Registry:
        data = self.driver.read(12)

        thermo_val = self.get_float(data, 0)
        pressure_val = self.get_float(data, 4)
        load_val = self.get_float(data, 8)

        print(thermo_val)
        print(pressure_val)
        print(load_val)
        print()

        state_field_registry.put("thermocouple", thermo_val)
        state_field_registry.put("pressure_gas", pressure_val)
        state_field_registry.put("load_cell_h20", load_val)
    
    def actuate(self, state_field_registry: Registry, flag: Flag) -> bool:
        pass
