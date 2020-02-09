from task import Task
from modules.drivers.arduino import Arduino

class Valve(Enum):
    BALL_VALVE_PRES: auto()
    BALL_VALVE_MAIN: auto()
    SOLENOID_VALVE_DRAIN: auto()
    SOLENOID_VALVE_DEPRES: auto()

# TODO: Do this
class ValveArduinoTask(Task):
    def __init__(self, flag: Flag):
        self.address = 0x08 ## Arduino address is 0x08
        self.arduino = Arduino("Valve Arduino", self.address)
        self.flag = flag

    def get_float(self, data, index):
        byte_array = bytes(data)
        return struct.unpack('f', byte_array)[0]

    def read(self, state_field_registry: Registry) -> Registry:
        data = self.arduino.read()
        ball_valve_pres = data[0:1]
        ball_valve_main = data[1:2]
        solenoid_valve_drain = data[2:3]
        solenoid_valve_depres = data[3:4]

        ball_valve_pres_val = self.get_float(data[0:1])
        ball_valve_main_val = self.get_float(data[1:2])
        solenoid_valve_drain_val = self.get_float(data[2:3])
        solenoid_valve_depres_val = self.get_float(data[3:4])

        state_field_registry.put("ball_valve_pres", ball_valve_pres_val)
        state_field_registry.put("ball_valve_main", ball_valve_main_val)
        state_field_registry.put("solenoid_valve_drain", solenoid_valve_drain_val)
        state_field_registry.put("solenoid_valve_depres", solenoid_valve_depres_val)

    def actuate():
        for key in flag.state_flags:
            if key == "ball_valve_pres":
                pass #actuate ball_valve_pres to flag["ball_valve_pres"]
            elif key == "ball_valve_main":
                pass #actuate ball_valve_main to flag["ball_valve_main"]
            elif key == "solenoid_valve_drain":
                pass #actuate solenoid_valve_drain to flag["solenoid_valve_drain"]
            elif key == "solenoid_valve_depres":
                pass #actuate solenoid_valve_depres to flag["solenoid_valve_depres"]
