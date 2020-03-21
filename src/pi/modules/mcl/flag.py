from modules.lib.mode import Mode
from modules.lib.errors import Error
from modules.lib.enums import ValveType, ValveLocation, ActuationType, Stage

class Flag:

    def __init__(self, config: dict):
        self.sensors = config["sensors"]["list"]
        self.valves = config["valves"]["list"]
        self.solenoids = self.valves[ValveType.SOLENOID]
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
                "actuation_type": {loc: ActuationType for loc in self.solenoids},
                "actuation_priority": {loc: int for loc in self.solenoids}
            },
        }


    def put(self, path: 'tuple', value, allow_error: bool = False) -> Error:
        flags, types = self.flags, self.types
        key = path[-1]
        path = path[:-1]
        for p in path:
            if p not in flags:
                if not allow_error:
                    raise Exception
                return Error.KEY_ERROR
            flags = flags[p]
            types = types[p]
        if key not in flags:
            if not allow_error:
                raise Exception
            return Error.KEY_ERROR
        if not isinstance(value, types[key]):
            if not allow_error:
                raise Exception
            return Error.KEY_ERROR
        flags[key] = value
        return Error.NONE


    def get(self, path: 'tuple', allow_error: bool = False) -> 'tuple':
        flag, types = self.flags, self.types
        for p in path:
            if p not in flag:
                if not allow_error:
                    raise Exception
                return Error.KEY_ERROR, None
            flag = flag[p]
        if isinstance(flag, dict):
            if not allow_error:
                raise Exception
            return Error.KEY_ERROR, None
        return Error.NONE, flag
