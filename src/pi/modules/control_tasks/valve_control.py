import time
from modules.mcl.flag import Flag
from modules.mcl.registry import Registry
from modules.lib.packet import Log, LogPriority
from modules.lib.enums import ActuationType, ValvePriority, ValveType

class ValveControl():
    def __init__(self, registry: Registry, flag: Flag):
        self.registry = registry
        self.flag = flag

    
    def begin(self, config: dict):
        self.config = config
        self.valves = self.config["valves"]["list"]
        self.send_interval = self.config["valves"]["send_interval"]
        self.last_send_time = None


    def send_valve_data(self):
        message = {}
        for valve_type in self.valves:
            message[valve_type] = {}
            for valve_loc in self.valves[valve_type]:
                _, val, _ = self.registry.get(("valve", valve_type, valve_loc))
                message[valve_type][valve_loc] = val
        log = Log(header="valve_data", message=message)
        _, enqueue = self.flag.get(("telemetry", "enqueue"))
        enqueue.append((log, LogPriority.INFO))
        print(log.to_string())
        self.flag.put(("telemetry", "enqueue"), enqueue)


    def abort(self):
        for valve_loc in self.valves["solenoid"]:
            actuation_type = self.registry.get(("valve_actuation", "actuation_type", ValveType.SOLENOID, valve_loc))[1]
            actuation_priority = self.registry.get(("valve_actuation", "actuation_priority", ValveType.SOLENOID, valve_loc))[1]
            if actuation_type != ActuationType.OPEN_VENT or actuation_priority != ValvePriority.ABORT_PRIORITY:
#                print("Hai")
                self.flag.put(("solenoid", "actuation_type", valve_loc), ActuationType.OPEN_VENT)
                self.flag.put(("solenoid", "actuation_priority", valve_loc), ValvePriority.ABORT_PRIORITY)


    def check_abort(self):
        if self.registry.get(("general", "hard_abort"))[1] or self.registry.get(("general", "soft_abort"))[1]:
            self.abort()


    def execute(self):
        self.check_abort()
#        print([self.registry.get(("valve", valve_type, valve_loc)) for valve_type in self.valves for valve_loc in self.valves[valve_type]])
        if self.last_send_time is None or time.time() - self.last_send_time > self.send_interval:
            self.send_valve_data()
            self.last_send_time = time.time()
        