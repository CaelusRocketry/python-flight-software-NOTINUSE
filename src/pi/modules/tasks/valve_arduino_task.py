from modules.tasks.task import Task
from modules.drivers.arduino import Arduino
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
import struct
from enum import Enum, auto

class Valve(Enum):
    BALL_VALVE_PRES: auto()
    BALL_VALVE_MAIN: auto()
    SOLENOID_VALVE_DRAIN: auto()
    SOLENOID_VALVE_DEPRES: auto()

class ValveArduinoTask(Task):
    def __init__(self):
        self.address = 0x08 ## Arduino address is 0x08
        self.arduino = Arduino("Valve Arduino", self.address)

    def get_float(self, data, index):
        byte_array = bytes(data)
        return struct.unpack('f', byte_array)[0]

    def read(self, state_field_registry: Registry, flag: Flag) -> Registry:
        data = self.arduino.read(4)

        ball_valve_pres_val = self.get_float(data[0])
        ball_valve_main_val = self.get_float(data[1])
        solenoid_valve_drain_val = self.get_float(data[2])
        solenoid_valve_depres_val = self.get_float(data[3])

        state_field_registry.put(("valve", "ball_valve_pres"), ball_valve_pres_val)
        state_field_registry.put(("valve", "ball_valve_main"), ball_valve_main_val)
        state_field_registry.put(("valve", "solenoid_valve_drain"), solenoid_valve_drain_val)
        state_field_registry.put(("valve", "solenoid_valve_depres"), solenoid_valve_depres_val)


    #TODO: Fix the structure of this method, it's completely different from other classes and won't work properly
    def actuate(self, state_field_registry: Registry, flag: Flag) -> Flag:
        for key in flag.state_flags:
            if key == "ball_valve_pres":
                pass #actuate ball_valve_pres to flag["ball_valve_pres"]
            elif key == "ball_valve_main":
                pass #actuate ball_valve_main to flag["ball_valve_main"]
            elif key == "solenoid_valve_drain":
                pass #actuate solenoid_valve_drain to flag["solenoid_valve_drain"]
            elif key == "solenoid_valve_depres":
                pass #actuate solenoid_valve_depres to flag["solenoid_valve_depres"]

        return flag