from modules.tasks.task import Task
from modules.drivers.arduino import Arduino
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
import struct

class SensorArduinoTask(Task):
    def __init__(self):
        self.name = "Sensor Arduino"

    def begin(self, config):
        self.address = 0x04
        self.arduino = Arduino("Arduino Sensor", self.address)

    def get_float(self, data, index):
        data = data[index:index+4]
        byte_array = bytes(data)
        return struct.unpack('f', byte_array)[0]

    def read(self, state_field_registry: Registry, flag: Flag) -> Registry:
        data = self.arduino.read(12)

        thermo_val = self.get_float(data, 0)
        pressure_val = self.get_float(data, 4)
        load_val = self.get_float(data, 8)

        state_field_registry.put(("sensor", "thermocouple"), thermo_val)
        state_field_registry.put(("sensor", "pressure_gas"), pressure_val)
        state_field_registry.put(("sensor", "load_cell_h20"), load_val)

        return state_field_registry
    
    def actuate(self, state_field_registry: Registry, flag: Flag) -> (Registry, Flag):
        return state_field_registry, flag
