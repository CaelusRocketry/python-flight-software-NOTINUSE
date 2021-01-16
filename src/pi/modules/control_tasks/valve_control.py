import time
from modules.mcl.flag import Flag
from modules.lib.helpers import enqueue
from modules.mcl.registry import Registry
from modules.lib.packet import Log, LogPriority
from modules.lib.enums import ActuationType, ValvePriority, ValveType, ValveLocation

class ValveControl():
    def __init__(self, registry: Registry, flag: Flag):
        # Initialize the ValveControl class
        self.registry = registry
        self.flag = flag

    
    def begin(self, config: dict):
        # Create basic varibales
        self.config = config
        self.valves = self.config["valves"]["list"]
        self.send_interval = self.config["valves"]["send_interval"]
        self.last_send_time = None
        # NOTE: Ground states are the same as abort states, meaning a valve's "natural" state (which is in the config) is the same as it's abort state
        # This is so that if the power dies for some reason, the valves will automatically abort
        self.aborted = False
        natural_to_actuation = {"OPEN": ActuationType.OPEN_VENT, "CLOSED": ActuationType.CLOSE_VENT}
        self.abort_actuations = {}
        for valve_loc in self.valves["solenoid"]:
            natural_str = self.valves["solenoid"][valve_loc]["natural"]
            natural = natural_to_actuation[natural_str]
            self.abort_actuations[valve_loc] = natural


    def send_valve_data(self):
        # Send the valve data to GS, basically a dict with the format: {solenoid: {loc1: "open", loc2: "closed"}}
        message = {}
        for valve_type in self.valves:
            message[valve_type] = {}
            for valve_loc in self.valves[valve_type]:
                _, val, _ = self.registry.get(("valve", valve_type, valve_loc))
                message[valve_type][valve_loc] = val
        log = Log(header="valve_data", message=message)
        enqueue(self.flag, log, LogPriority.INFO)


    def abort(self):
        # Loop through all the solenoid valves
        for valve_loc in self.valves["solenoid"]:
            actuation_type = self.registry.get(("valve_actuation", "actuation_type", ValveType.SOLENOID, valve_loc))[1]
            actuation_priority = self.registry.get(("valve_actuation", "actuation_priority", ValveType.SOLENOID, valve_loc))[1]
            # If the valve hasn't been aborted, then abort it.
            if actuation_priority != ValvePriority.ABORT_PRIORITY:
                self.flag.put(("solenoid", "actuation_type", valve_loc), self.abort_actuations[valve_loc])
                self.flag.put(("solenoid", "actuation_priority", valve_loc), ValvePriority.ABORT_PRIORITY)


    def undo_abort(self):
        # Loop through all the solenoid valves
        for valve_loc in self.valves["solenoid"]:
            actuation_priority = self.registry.get(("valve_actuation", "actuation_priority", ValveType.SOLENOID, valve_loc))[1]
            # This if statement should technically be true for all valves, but basically it just makes sure that the valve aborted.
            if actuation_priority == ValvePriority.ABORT_PRIORITY:
                # Reset the valve priority to zero. This means that whatever the Pi tells it to do next, it'll do that, instead of sticking to its aborted state.
                self.flag.put(("solenoid", "actuation_type", valve_loc), ActuationType.NONE)
                self.flag.put(("solenoid", "actuation_priority", valve_loc), ValvePriority.NONE)


    def check_abort(self):
        # If you just got a message to abort, then abort
        if self.registry.get(("general", "soft_abort"))[1] and not self.aborted:
            self.abort()
            self.aborted = True
        # If you just got a message to undo abort, then undo abort
        elif not self.registry.get(("general", "soft_abort"))[1] and self.aborted:
            self.undo_abort()
            self.aborted = False


    def execute(self):
        # Check if the rocket has been aborted (and act correspondingly)
        self.check_abort()
        # Send valve data every once in a while to update GS
        if self.last_send_time is None or time.time() - self.last_send_time > self.send_interval:
            self.send_valve_data()
            self.last_send_time = time.time()
        