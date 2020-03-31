from modules.tasks.task import Task
from modules.drivers.arduino import Arduino
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.lib.enums import ValveType, SolenoidState, ActuationType, ValvePriority
import struct
from enum import Enum, auto

class ValveTask(Task):
    def __init__(self, registry: Registry, flag: Flag):
        self.name = "Valve Arduino"
        self.registry = registry
        self.flag = flag
        self.actuation_dict = {0: ActuationType.NONE, 1: ActuationType.OPEN_VENT, 2: ActuationType.CLOSE_VENT, 3: ActuationType.PULSE}
        self.state_dict = {0: SolenoidState.OPEN, 1: SolenoidState.CLOSED}
        self.num_actuation_types = len(self.actuation_types)


    def begin(self, config):
        self.config = config["valves"]
        #TODO: Make sure that this is the same order that the arduino returns its data in
        self.valves = self.config["list"]
        self.solenoids = [loc for loc in self.valves[ValveType.SOLENOID]]
        self.num_solenoids = len(self.solenoids)
        self.arduino = Arduino(self.name, self.config)


    def get_solenoid_state(self, val):
        return self.state_dict[val] if val in state_dict else None


    def get_actuation_type(self, val):
        return self.actuation_dict[val] if val in actuation_dict else None


    def get_float(self, data):
        byte_array = bytes(data)
        return struct.unpack('f', byte_array)[0]


    def get_command(self, loc, actuation_type):
        #Formula: idx1 * 16 + idx2
        loc_idx = self.solenoids.index(loc)
        inv_actuations = {v:k for k,v in zip(self.actuation_dict)}
        actuation_idx = inv_actuations[actuation_type]
        return loc_idx*16 + actuation_idx


    def read(self):
        data = self.arduino.read(self.num_solenoids*2)

        solenoid_states = [self.get_solenoid_state(val) for val in data[::2]]
        actuation_types = [self.get_actuation_type(val) for val in data[1::2]]
        assert(None not in solenoid_states)
        assert(None not in actuation_types)
        assert(len(solenoid_states) == self.num_solenoids)
        assert(len(actuation_types) == self.num_solenoids)

        for idx in range(self.num_solenoids):
            valve_loc = self.solenoids[idx]
            self.registry.put(("valve", ValveType.SOLENOID, valve_loc), solenoid_states[idx])
            self.registry.put(("valve_actuation", "actuation_type", ValveType.SOLENOID, valve_loc), actuation_types[idx])
            if actuation_types[idx] == ActuationType.NONE:
                self.registry.put(("valve_actuation", "actuation_priority", ValveType.SOLENOID, valve_loc), ValvePriority.NONE)


    def actuate_solenoids(self):
        for loc in self.solenoids:
            _, actuation_type = self.flag.get(("solenoid", "actuation_type", loc))
            if actuation_type != ActuationType.NONE:
                _, actuation_priority = self.flag.get(("solenoid", "actuation_priority", loc))
                _, curr_priority, _ = self.registry.get(("valve_actuation", "actuation_priority", ValveType.SOLENOID, loc))
                #TODO: Decide, >= or > ?
                print(actuation_priority, curr_priority)
                if actuation_priority >= curr_priority:
                    print("Actuating")
                    command = self.get_command(loc, actuation_type)
                    self.arduino.write(command)
                    self.registry.put(("valve_actuation", "actuation_type", ValveType.SOLENOID, loc), actuation_type)
                    self.registry.put(("valve_actuation", "actuation_priority", ValveType.SOLENOID, loc), actuation_priority)
                    self.flag.put(("solenoid", "actuation_type", loc), ActuationType.NONE)
                    self.flag.put(("solenoid", "actuation_priority", loc), ValvePriority.NONE)


    def abort(self):
        for loc in self.solenoids:
            self.flag.put(("solenoid", "actuation_type", loc), ActuationType.OPEN_VENT)
            self.flag.put(("solenoid", "actuation_priority", loc), ValvePriority.ABORT_PRIORITY)


    def check_abort(self):
        if self.flag.get(("general", "hard_abort"))[1]:
            self.registry.put(("general", "hard_abort"), True)
            self.abort()
        elif self.flag.get(("general", "soft_abort"))[1]:
            self.registry.put(("general", "soft_abort"), True)
            self.abort()

        self.flag.put(("general", "hard_abort"), False)
        self.flag.put(("general", "soft_abort"), False)


    #TODO: Fix the structure of this method, it's completely different from other classes and won't work properly
    def actuate(self):
        self.check_abort()
        if self.registry.get(("general", "soft_abort"))[1] or self.registry.get(("general", "hard_abort"))[1]:
            # Can't actuate if the rocket's been aborted
            return

        self.actuate_solenoids()
