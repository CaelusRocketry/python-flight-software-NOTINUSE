from modules.lib.mode import Mode
from modules.lib.errors import AccessError
from modules.lib.enums import ValveLocation, ActuationType

class Flag:

    def __init__(self):
        self.state_flags = {
            "abort": {
                "hard_abort": [],
                "soft_abort": []
            },
            "progress": {
                "stage": None
            },
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
            "solenoid": {
                "actuation_type": {
                    ValveLocation.PRESSURE_RELIEF: ActuationType.NONE,
                    ValveLocation.PROPELLANT_VENT: ActuationType.NONE,
                    ValveLocation.MAIN_PROPELLANT_VALVE: ActuationType.NONE
                },
                "actuation_priority": {
                    ValveLocation.PRESSURE_RELIEF: 0,
                    ValveLocation.PROPELLANT_VENT: 0,
                    ValveLocation.MAIN_PROPELLANT_VALVE: 0
                }
            },
        }

        self.state_types = {
            "abort": {
                "hard_abort": list,
                "soft_abort": list
            },
            "progress": {
                "stage": Stage
            },
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
            "solenoid": {
                "actuation_type": {
                    ValveLocation.PRESSURE_RELIEF: ActuationType,
                    ValveLocation.PROPELLANT_VENT: ActuationType,
                    ValveLocation.MAIN_PROPELLANT_VALVE: ActuationType
                },
                "actuation_priority": {
                    ValveLocation.PRESSURE_RELIEF: int,
                    ValveLocation.PROPELLANT_VENT: int,
                    ValveLocation.MAIN_PROPELLANT_VALVE: int
                }
            },
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