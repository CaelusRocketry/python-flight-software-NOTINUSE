from pi.modules.lib.enums import SensorStatus, ActuationType, ValvePriority, ValveLocation, SensorLocation, SolenoidState, SensorStatus
from pi.modules.mcl.registry import Registry
from pi.modules.mcl.flag import Flag

class PressureControl():
    def __init__(self, registry: Registry, flag: Flag):
        print("Pressure Control")
        self.registry = registry
        self.flag = flag
        

    def begin(self, config: dict):
        self.config = config
        self.valves = config["valves"]["list"]["solenoid"]
        self.sensors = config["sensors"]["list"]["pressure"]
        self.matchups = [(SensorLocation.TANK, ValveLocation.PRESSURE_RELIEF)]


    def execute(self):
        self.check_pressure()

    def check_pressure(self):
        #TODO: make sure that pressure relief is the right valve
        for sensor_loc, valve_loc in self.matchups:
            if self.registry.get(("sensor_normalized", "pressure", sensor_loc)) >= self.sensors[sensor_loc]["boundaries"][1]:
                if self.registry.get(("solenoid", "valve", valve_loc)) == SolenoidState.CLOSED:
                    self.registry.put(("solenoid", "actuation_type", valve_loc), ActuationType.OPEN_VENT)
                    self.registry.put(("solenoid", "actuation_priority", valve_loc), ValvePriority.PI_PRIORITY)

            else if self.registry.get(("sensor_status", "pressure", sensor_loc)) == SensorStatus.SAFE:
                if self.registry.get(("solenoid", "valve", valve_loc)) == SolenoidState.OPEN:
                    self.registry.put(("solenoid", "actuation_type", valve_loc), ActuationType.CLOSE_VENT)
                    self.registry.put(("solenoid", "actuation_priority", valve_loc), ValvePriority.PI_PRIORITY)
            
