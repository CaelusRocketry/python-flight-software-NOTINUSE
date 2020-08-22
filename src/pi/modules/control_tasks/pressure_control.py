from modules.lib.enums import SensorStatus, ActuationType, ValvePriority, ValveLocation, SensorLocation, SolenoidState, SensorStatus, ValveType
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag

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
        # print("PRESSURE CONTROL")
        for sensor_loc, valve_loc in self.matchups:
            if self.registry.get(("sensor_normalized", "pressure", sensor_loc))[1] > self.sensors[sensor_loc]["boundaries"]["safe"][1]:
                print("PRESSURE TOO HIGH")
                if self.registry.get(("valve", "solenoid", valve_loc))[1] == SolenoidState.CLOSED:
                    print("OPENING")
                    self.flag.put(("solenoid", "actuation_type", valve_loc), ActuationType.OPEN_VENT)
                    self.flag.put(("solenoid", "actuation_priority", valve_loc), ValvePriority.PI_PRIORITY)

            elif self.registry.get(("sensor_status", "pressure", sensor_loc))[1] == SensorStatus.SAFE:
                if self.registry.get(("valve", "solenoid", valve_loc))[1] == SolenoidState.OPEN:
                    self.flag.put(("solenoid", "actuation_type", valve_loc), ActuationType.CLOSE_VENT)
                    self.flag.put(("solenoid", "actuation_priority", valve_loc), ValvePriority.PI_PRIORITY)
            
