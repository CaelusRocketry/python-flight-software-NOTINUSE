from pi.modules.lib.enums import SensorStatus, ActuationType, ValvePriority
from pi.modules.mcl.registry import Registry
from pi.modules.mcl.flag import Flag

class PressureControl():
    def __init__(self, registry: Registry, flag: Flag, config: dict):
        print("Pressure Control")
        self.registry = registry
        self.flag = flag
        self.valves = config["valves"]["list"]["solenoid"]

    def begin(self):
        pass

    def execute(self):
        self.check_pressure()

    def check_pressure(self):
        #TODO: make sure that pressure relief is the right valve
        for loc in self.valves:
            if self.registry.get(("sensor_status", "pressure", loc)) == SensorStatus.CRITICAL:
                self.registry.put(("solenoid", "actuation_type", "pressure_relief"), ActuationType.OPEN_VENT)
                self.registry.put(("solenoid", "actuation_priority", "pressure_relief"), ValvePriority.MAX_TELEMETRY_PRIORITY)
