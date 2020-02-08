from mode import Mode
from errors import FlagError

class Flag:

    def __init__(self):
        self.state_flags = {
            "state_put_error": None,
            "state_get_error": None,
            "flag_put_error": None,
            "flag_get_error": None,
            "ball_valve_pres": None,
            "ball_valve_main": None,
            "solenoid_valve_drain": None,
            "solenoid_valve_depres": None,
        }

        self.state_types = {
            "state_put_error": bool,
            "state_get_error": bool,
            "flag_put_error": bool,
            "flag_get_error": bool,
            "ball_valve_pres": int,
            "ball_valve_main": int,
            "solenoid_valve_drain": bool,
            "solenoid_valve_depres": bool,
        }

    def put(key, value) -> SetError:
        if key not in self.state_flags:
            self.state_flags["flag_put_error"] = True
            return False
        self.state_flags[key] = value
        return True
        

    def get(key):
        if key not in self.state_flags:
            self.state_flags["flag_get_error"] = True
            return False
        return self.state_flags[key]