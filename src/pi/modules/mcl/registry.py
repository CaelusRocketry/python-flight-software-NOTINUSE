from modules.lib.mode import Mode
from modules.lib.packet import Packet
from modules.lib.enums import SensorStatus
from modules.lib.errors import AccessError
# from modules.lib.encoding import EnumEncoder
import time
import json

class Registry:


    # TODO: Add IMU data, Pressure data, Load cell data, and Valve data to SFR
    def __init__(self):
        self.values = {
            "sensor": {
                "thermocouple": None,
                "thermocouple_status": SensorStatus.SAFE,
                "pressure_gas": None,
                "load_cell_h20": None,
                "thermocouple_chamber": None,
                "thermocouple_tank": None,
                "pressure_chamber": None,
                "pressure_tank": None,
                "pressure_injector": None,
                "load_tank": None
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
                "thermocouple": float,
                "thermocouple_status": SensorStatus,
                "pressure_gas": float,
                "load_cell_h20": float,
                "thermocouple_chamber": float,
                "thermocouple_tank": float,
                "pressure_chamber": float,
                "pressure_tank": float,
                "pressure_injector": float,
                "load_tank": float,
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

    def put(self, key: 'tuple', value) -> AccessError:
        outer, inner = key
        if outer not in self.values:
            return AccessError.PUT_ERROR
        if inner not in self.values[outer]:
            return AccessError.PUT_ERROR
        if not isinstance(value, self.types[outer][inner]):
            return AccessError.KEY_ERROR
        self.values[outer][inner] = value
        self.times[outer][inner] = time.time()
        return AccessError.NONE

    def get(self, key):
        outer, inner = key
        if outer not in self.values:
            return AccessError.KEY_ERROR
        if inner not in self.values[outer]:
            return AccessError.KEY_ERROR
        return self.values[outer][inner]

    def to_string(self):
        return json.dumps(self.values, cls=EnumEncoder)
    