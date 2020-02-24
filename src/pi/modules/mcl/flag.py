from modules.lib.mode import Mode
from modules.lib.errors import AccessError

class Flag:

    def __init__(self):
        self.state_flags = {
            "telemetry": {
                "send_queue": [],
                "reset": True
            },
            "error": {
                "state_put_error": None,
                "state_get_error": None,
                "flag_put_error": None,
                "flag_get_error": None,
            },
            "valve": {
                "ball_valve_pres": None,
                "ball_valve_main": None,
                "solenoid_valve_drain": None,
                "solenoid_valve_depres": None,
            }
        }

        self.state_types = {
            "telemetry": {
                "send_queue": list,
                "reset": bool
            },
            "error": {
                "state_put_error": bool,
                "state_get_error": bool,
                "flag_put_error": bool,
                "flag_get_error": bool,
            },
            "valve": {
                "ball_valve_pres": int,
                "ball_valve_main": int,
                "solenoid_valve_drain": bool,
                "solenoid_valve_depres": bool,
            }
        }

    def put(self, key: 'tuple', value) -> AccessError:
        outer, inner = key
        if outer not in self.state_flags:
            print("OUTER ERROR")
            return AccessError.KEY_ERROR
        if inner not in self.state_flags[outer]:
            print("INNER ERROR", key)
            return AccessError.KEY_ERROR
        self.state_flags[outer][inner] = value
        return AccessError.NONE


    def get(self, key: 'tuple'):
        outer, inner = key
        if outer not in self.state_flags:
            return AccessError.KEY_ERROR
        if inner not in self.state_flags[outer]:
            return AccessError.KEY_ERROR
        return self.state_flags[outer][inner]