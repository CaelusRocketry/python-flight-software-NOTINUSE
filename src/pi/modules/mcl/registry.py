from modules.lib.mode import Mode
from modules.lib.packet import Packet
from modules.lib.enums import SensorStatus
from modules.lib.errors import AccessError
from modules.lib.enums import SolenoidState, ValveType, ValveLocation, SensorType, SensorLocation
# from modules.lib.encoding import EnumEncoder
import time
import json

class Registry:


    # TODO: Add IMU data, Pressure data, Load cell data, and Valve data to SFR
    def __init__(self):
        self.values = {
            "sensor": {
                SensorType.THERMOCOUPLE: {
                    SensorLocation.CHAMBER: None,
                    SensorLocation.TANK: None
                },
                SensorType.PRESSURE: {
                    SensorLocation.CHAMBER: None,
                    SensorLocation.INJECTOR: None
                },
                SensorType.LOAD: {
                    SensorLocation.TANK: None,
                    SensorLocation.INJECTOR: None
                }
            },
            "sensor_status": {
                SensorType.THERMOCOUPLE: {
                    SensorLocation.CHAMBER: None,
                    SensorLocation.TANK: None
                },
                SensorType.PRESSURE: {
                    SensorLocation.CHAMBER: None,
                    SensorLocation.INJECTOR: None
                },
                SensorType.LOAD: {
                    SensorLocation.TANK: None,
                    SensorLocation.INJECTOR: None
                }
            },
            "valve": {
                ValveType.SOLENOID: {
                    ValveLocation.PRESSURE_RELIEF: SolenoidState.CLOSED,
                    ValveLocation.PROPELLANT_VENT: SolenoidState.CLOSED,
                    ValveLocation.MAIN_PROPELLANT_VALVE: SolenoidState.CLOSED
                }
            },
            "valve_actuation": {
                "actuation_type": {
                    ValveType.SOLENOID: {
                        ValveLocation.PRESSURE_RELIEF: ActuationType.NONE,
                        ValveLocation.PROPELLANT_VENT: ActuationType.NONE,
                        ValveLocation.MAIN_PROPELLANT_VALVE: ActuationType.NONE
                    }
                },
                "actuation_priority": {
                    ValveType.SOLENOID: {
                        ValveLocation.PRESSURE_RELIEF: 0,
                        ValveLocation.PROPELLANT_VENT: 0,
                        ValveLocation.MAIN_PROPELLANT_VALVE: 0
                    }
                }
            },
            "telemetry": {
                "ingest_queue": [],
                "status": None
            },
            "general": {
                "mode": None
            }
        }
        self.types = {
            "sensor": {
                SensorType.THERMOCOUPLE: {
                    SensorLocation.CHAMBER: (float, SensorStatus),
                    SensorLocation.TANK: (float, SensorStatus)
                },
                SensorType.PRESSURE: {
                    SensorLocation.CHAMBER: (float, SensorStatus),
                    SensorLocation.INJECTOR: (float, SensorStatus)
                },
                SensorType.LOAD: {
                    SensorLocation.TANK: (float, SensorStatus),
                    SensorLocation.INJECTOR: (float, SensorStatus)
                }
            },
            "sensor_status": {
                SensorType.THERMOCOUPLE: {
                    SensorLocation.CHAMBER: SensorStatus,
                    SensorLocation.TANK: SensorStatus
                },
                SensorType.PRESSURE: {
                    SensorLocation.CHAMBER: SensorStatus,
                    SensorLocation.TANK: SensorStatus,
                    SensorLocation.INJECTOR: SensorStatus
                },
                SensorType.LOAD: {
                    SensorLocation.TANK: SensorStatus,
                }
            },
            "valve": {
                ValveType.SOLENOID: {
                    ValveLocation.PRESSURE_RELIEF: SolenoidState,
                    ValveLocation.PROPELLANT_VENT: SolenoidState,
                    ValveLocation.MAIN_PROPELLANT_VALVE: SolenoidState
                },
            },
            "valve_actuation": {
                "actuation_type": {
                    ValveType.SOLENOID: {
                        ValveLocation.PRESSURE_RELIEF: ActuationType,
                        ValveLocation.PROPELLANT_VENT: ActuationType,
                        ValveLocation.MAIN_PROPELLANT_VALVE: ActuationType
                    }
                },
                "actuation_priority": {
                    ValveType.SOLENOID: {
                        ValveLocation.PRESSURE_RELIEF: int,
                        ValveLocation.PROPELLANT_VENT: int,
                        ValveLocation.MAIN_PROPELLANT_VALVE: int
                    }
                }
            },
            "telemetry": {
                "ingest_queue": list,
                "status": bool,
                "resetting": bool
            },
            "general": {
                "mode": Mode
            }
        }
        self.times = {i: {j: None for j in i} for i in self.values}

    def put(self, path: 'tuple', value) -> AccessError:
        values, types, times = self.values, self.types, self.times
        key = path[-1]
        path = path[:-1]
        for p in path:
            if p not in values:
                return AccessError.KEY_ERROR
            values = values[p]
            types = types[p]
            times = times[p]
        if not isinstance(values[key], types[key]):
            return AccessError.KEY_ERROR
        values[key] = value
        times[key] = time.time()
        return AccessError.NONE

    def get(self, path) -> tuple:
        values, times = self.values, self.times
        for p in path:
            if p not in values:
                return AccessError.KEY_ERROR, None, None
            values = values[p]
            times = times[p]
        return AccessError.NONE, values, times

    def to_string(self):
        return json.dumps(self.values, cls=EnumEncoder)
    