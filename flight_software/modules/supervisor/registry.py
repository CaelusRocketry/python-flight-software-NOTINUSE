from mode import Mode
from status import Status
from errors import SFRError
import time

class Registry:


    # TODO: Add IMU data, Pressure data, Load cell data, and Valve data to SFR
    def __init__(self, flag: Flag):
        self.flag = flag
        self.values = {
            "thermocouple": None,
            "thermocouple_status": Status.WORKING,
            "telemetry_queue": [],
            "mode": None
        }
        self.types = {
            "thermocouple": None,
            "thermocouple_status": Status,
            "telemetry_queue": list,
            "mode": Mode
        }
        self.times = {i: None for i in self.values}

    def put(key, value) -> SetError:
        if key not in self.values:
            self.flag.state_flags["state_put_error"] = True
            return SetError.PUT_ERROR
        if not isinstance(value, self.types[key]):
            return SetError.PUT_ERROR
        self.values[key] = value
        self.times[key] = time.time()
        return SFRError.NONE

    def get(key):
        if key not in self.values:
            self.flag.state_flags["state_get_error"] = True
            return Error.ERROR
        return self.values[key]

