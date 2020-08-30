import time
from modules.mcl.flag import Flag
from modules.lib.helpers import enqueue
from modules.mcl.registry import Registry
from modules.lib.packet import Log, LogPriority
from modules.lib.enums import ActuationType, ValvePriority, ValveType, ValveLocation

class ValveControl():
    def __init__(self, registry: Registry, flag: Flag):
        self.registry = registry
        self.flag = flag

    
    def begin(self, config: dict):
        self.config = config
        self.valves = self.config["valves"]["list"]
        self.send_interval = self.config["valves"]["send_interval"]
        self.last_send_time = None
        # NOTE: Ground states are the same as abort states, meaning a valve's "natural" state (which is in the config) is the same as it's abort state
        # This is so that if the power dies for some reason, the valves will automatically abort
        natural_to_actuation = {"OPEN": ActuationType.OPEN_VENT, "CLOSED": ActuationType.CLOSE_VENT}
        self.abort_actuations = {}
        for valve_loc in self.valves["solenoid"]:
            natural_str = self.valves["solenoid"][valve_loc]["natural"]
            natural = natural_to_actuation[natural_str]
            self.abort_actuations[valve_loc] = natural


    def send_valve_data(self):
        message = {}
        for valve_type in self.valves:
            message[valve_type] = {}
            for valve_loc in self.valves[valve_type]:
                _, val, _ = self.registry.get(("valve", valve_type, valve_loc))
                message[valve_type][valve_loc] = val
        log = Log(header="valve_data", message=message)
        enqueue(self.flag, log, LogPriority.INFO)


    def abort(self):
        for valve_loc in self.valves["solenoid"]:
            actuation_type = self.registry.get(("valve_actuation", "actuation_type", ValveType.SOLENOID, valve_loc))[1]
            actuation_priority = self.registry.get(("valve_actuation", "actuation_priority", ValveType.SOLENOID, valve_loc))[1]
            if actuation_type != self.abort_actuations[valve_loc] or actuation_priority != ValvePriority.ABORT_PRIORITY:
                self.flag.put(("solenoid", "actuation_type", valve_loc), self.abort_actuations[valve_loc])
                self.flag.put(("solenoid", "actuation_priority", valve_loc), ValvePriority.ABORT_PRIORITY)


    def undo_abort(self):
        for valve_loc in self.valves["solenoid"]:
            actuation_priority = self.registry.get(("valve_actuation", "actuation_priority", ValveType.SOLENOID, valve_loc))[1]
            if actuation_priority == ValvePriority.ABORT_PRIORITY:
                self.flag.put(("solenoid", "actuation_type", valve_loc), ActuationType.NONE)
                self.flag.put(("solenoid", "actuation_priority", valve_loc), ValvePriority.ABORT_PRIORITY)


    def check_abort(self):
        if self.registry.get(("general", "hard_abort"))[1] or self.registry.get(("general", "soft_abort"))[1]:
            self.abort()
        elif not self.registry.get(("general", "soft_abort"))[1]:
            self.undo_abort()


    def execute(self):
        self.check_abort()
        if self.last_send_time is None or time.time() - self.last_send_time > self.send_interval:
            self.send_valve_data()
            self.last_send_time = time.time()
        