from modules.lib.mode import Mode
from modules.lib.errors import Error
from modules.lib.enums import ValveLocation, ActuationType, Stage

class Flag:

    def __init__(self):
        self.solenoids = [ValveLocation.PRESSURE_RELIEF,
                        ValveLocation.PROPELLANT_VENT, ValveLocation.MAIN_PROPELLANT_VALVE]
        self.flags = {
            "abort": {
                "hard_abort": [],
                "soft_abort": []
            },
            "progress": {
                "stage": None
            },
            "telemetry": {
                "enqueue": [],
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
                "actuation_type": {loc: ActuationType.NONE for loc in self.solenoids},
                "actuation_priority": {loc: 0 for loc in self.solenoids}
            },
        }

        self.types = {
            "abort": {
                "hard_abort": list,
                "soft_abort": list
            },
            "progress": {
                "stage": Stage
            },
            "telemetry": {
                "send_queue": list,
                "enqueue": list,
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

    def put(self, path: 'tuple', value) -> Error:
        flags, types = self.flags, self.types
        key = path[-1]
        path = path[:-1]
        for p in path:
            if p not in flags:
                return Error.KEY_ERROR
            flags = flags[p]
            types = types[p]
        if key not in flags:
            return Error.KEY_ERROR
        if not isinstance(value, types[key]):
            return Error.KEY_ERROR
        flags[key] = value
        return Error.NONE


    def get(self, path: 'tuple') -> 'tuple':
        flag, types = self.flags, self.types
        for p in path:
            if p not in flag:
                return Error.KEY_ERROR, None
            flag = flag[p]
        if isinstance(flag, dict):
            return Error.KEY_ERROR, None
        return Error.NONE, flag