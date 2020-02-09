from task import Task
from abc import ABC, abstractmethod
from modules.drivers.arduino import Arduino
from modules.supervisor.command import Command
from modules.supervisor.registry import Registry
from modules.supervisor.flags import Flag
from modules.drivers.imu_driver import IMU

class SensorArduinoTask(Task):
    def __init__(self, flag: Flag):
        self.address = 0x04
        self.arduino = Arduino("Sensor Arduino", self.address)
        self.flag = flag

    def get_float(self, data, index):
            byte_array = bytes(data)
            return struct.unpack('f', byte_array)[0]

    def read(self, state_field_registry: Registry) -> Registry:
        data = self.arduino.read()
        thermo_data = data[0:4]
        pressure_data = data[4:8]
        load_data = data[8:12]

        thermo_val = self.get_float(thermo_data)
        pressure_val = self.get_float(pressure_data)
        load_val = self.get_float(load_data)

        state_field_registry.put("thermocouple", thermo_val)
        state_field_registry.put("pressure_gas", pressure_val)
        state_field_registry.put("load_cell_h20", load_val)
    
    def actuate(self, command: Command) -> bool:
        pass