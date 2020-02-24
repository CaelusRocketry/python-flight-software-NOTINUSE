from modules.lib.mode import Mode
from modules.lib.status import Status
from modules.lib.errors import AccessError
from modules.lib.logging import Packet
import time

class Registry:


    # TODO: Add IMU data, Pressure data, Load cell data, and Valve data to SFR
    def __init__(self):
        self.values = {
            "sensor": {
                "thermocouple": None,
                "thermocouple_status": Status.WORKING,
                "pressure_gas": None,
                "load_cell_h20": None,
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
                "thermocouple_status": Status,
                "pressure_gas": float,
                "load_cell_h20": float,
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
            return AccessError.PUT_ERROR
        if inner not in self.values[outer]:
            return AccessError.PUT_ERROR
        return self.values[outer][inner]

