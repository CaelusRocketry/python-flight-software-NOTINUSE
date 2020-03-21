from modules.lib.packet import Packet
from modules.lib.enums import SensorStatus
from modules.lib.errors import Error
from modules.lib.enums import SolenoidState, ValveType, ValveLocation, SensorType, SensorLocation, ActuationType, Stage, ValvePriority
import time
import json


class Registry:

    # TODO: Add IMU data, Pressure data, Load cell data, and Valve data to SFR
    def __init__(self, config: dict):
        self.sensors = config["sensors"]["list"]
        self.valves = config["valves"]["list"]
        self.values = {
            "sensor": {s_type: {loc: None for loc in self.sensors[s_type]} for s_type in self.sensors},
            "sensor_status": {s_type: {loc: None for loc in self.sensors[s_type]} for s_type in self.sensors},
            "valve": {v_type: {loc: SolenoidState.CLOSED for loc in self.valves[v_type]} for v_type in self.valves},
            "valve_actuation": {
                "actuation_type": {v_type: {loc: ActuationType.NONE for loc in self.valves[v_type]} for v_type in self.valves},
                "actuation_priority": {v_type: {loc: ValvePriority.NONE for loc in self.valves[v_type]} for v_type in self.valves}
            },
            "telemetry": {
                "ingest_queue": [],
                "status": None
            },
            "general": {
                "hard_abort": False,
                "soft_abort": False,
                "stage": None
            }
        }

        self.types = {
            "sensor": {s_type: {loc: float for loc in self.sensors[s_type]} for s_type in self.sensors},
            "sensor_status": {s_type: {loc: SensorStatus for loc in self.sensors[s_type]} for s_type in self.sensors},
            "valve": {v_type: {loc: SolenoidState for loc in self.valves[v_type]} for v_type in self.valves},
            "valve_actuation": {
                "actuation_type": {v_type: {loc: ActuationType for loc in self.valves[v_type]} for v_type in self.valves},
                "actuation_priority": {v_type: {loc: ValvePriority for loc in self.valves[v_type]} for v_type in self.valves}
            },
            "telemetry": {
                "ingest_queue": list,
                "status": bool,
                "resetting": bool
            },
            "general": {
                "hard_abort": bool,
                "soft_abort": bool,
                "stage": Stage
            }
        }

        self.times = {
            "sensor": {s_type: {loc: None for loc in self.sensors[s_type]} for s_type in self.sensors},
            "sensor_status": {s_type: {loc: None for loc in self.sensors[s_type]} for s_type in self.sensors},
            "valve": {v_type: {loc: None for loc in self.valves[v_type]} for v_type in self.valves},
            "valve_actuation": {
                "actuation_type": {v_type: {loc: None for loc in self.valves[v_type]} for v_type in self.valves},
                "actuation_priority": {v_type: {loc: None for loc in self.valves[v_type]} for v_type in self.valves}
            },
            "telemetry": {
                "ingest_queue": None,
                "status": None,
                "resetting": None
            },
            "general": {
                "hard_abort": None,
                "soft_abort": None,
                "stage": None
            }
        }

    def put(self, path: tuple, value, allow_error: bool = False) -> Error:
        values, types, times = self.values, self.types, self.times
        key = path[-1]
        path = path[:-1]
        for p in path:
            if p not in values:
                if not allow_error:
                    raise Exception
                return Error.KEY_ERROR
            values = values[p]
            types = types[p]
            times = times[p]
        if key not in values:
            if not allow_error:
                raise Exception
            return Error.KEY_ERROR
        if not isinstance(value, types[key]):
            if not allow_error:
                raise Exception
            return Error.KEY_ERROR
        values[key] = value
        times[key] = time.time()
        return Error.NONE

    def get(self, path: tuple, allow_error: bool = False) -> tuple:
        values, times = self.values, self.times
        for p in path:
            if p not in values:
                if not allow_error:
                    raise Exception
                    print(1/0)
                return Error.KEY_ERROR, None, None
            values = values[p]
            times = times[p]
        
        # Don't allow the user to get part of the registry, they can only get endpoints
        # TODO: Decide if this is somethign to keep or nah
        if isinstance(values, dict):
            if not allow_error:
                raise Exception
            return Error.KEY_ERROR, None
        return Error.NONE, values, times

    def to_string(self):
        return json.dumps(self.values)
