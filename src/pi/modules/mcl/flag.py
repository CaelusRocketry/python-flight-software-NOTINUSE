from modules.lib.mode import Mode
from modules.lib.errors import Error
from modules.lib.enums import ValveType, ValveLocation, ActuationType, ValvePriority

class Flag:

    def __init__(self, config: dict):
        self.sensors = config["sensors"]["list"]
        self.valves = config["valves"]["list"]
        self.solenoids = self.valves[ValveType.SOLENOID]
        self.flags = {
            "general": {
                "hard_abort": False,
                "soft_abort": False,
                "progress": False
            },
            "telemetry": {
                "enqueue": [],
                "send_queue": [],
                "reset": True
            },
            "solenoid": {
                "actuation_type": {loc: ActuationType.NONE for loc in self.solenoids},
                "actuation_priority": {loc: ValvePriority.NONE for loc in self.solenoids}
            },
        }

        self.types = {
            "general": {
                "hard_abort": bool,
                "soft_abort": bool,
                "progress": bool
            },
            "telemetry": {
                "send_queue": list,
                "enqueue": list,
                "reset": bool
            },
            "solenoid": {
                "actuation_type": {loc: ActuationType for loc in self.solenoids},
                "actuation_priority": {loc: ValvePriority for loc in self.solenoids}
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
