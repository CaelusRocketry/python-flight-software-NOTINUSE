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
        self.actuation_dict = {0: ActuationType.NONE, 1: ActuationType.CLOSE_VENT, 2: ActuationType.OPEN_VENT, 3: ActuationType.PULSE}
        self.inv_actuations = {self.actuation_dict[k]:k for k in self.actuation_dict}
        self.state_dict = {0: SolenoidState.OPEN, 1: SolenoidState.CLOSED}


    def begin(self, config):
        self.config = config["valves"]
        #TODO: Make sure that this is the same order that the arduino returns its data in
        self.valves = self.config["list"]
        self.solenoids = [loc for loc in self.valves[ValveType.SOLENOID]]
        self.num_solenoids = len(self.solenoids)
        self.arduino = Arduino(self.name, self.config)


    def get_solenoid_state(self, val):
        assert(val in self.state_dict)
        return self.state_dict[val]


    def get_actuation_type(self, val):
        assert(val in self.actuation_dict)
        return self.actuation_dict[val]


    def get_float(self, data):
        byte_array = bytes(data)
        return struct.unpack('f', byte_array)[0]


    def get_command(self, loc, actuation_type):
        # Message structure: [loc, actuation type]
        loc_idx = self.solenoids.index(loc)
        actuation_idx = self.inv_actuations[actuation_type]
        return [loc_idx, actuation_idx]


    def read(self):
        byte_data = self.arduino.read(self.num_solenoids*2)
        int_data = int.from_bytes(byte_data, 'big')

        override = True if int_data & 0b1 else False
        int_data = int_data >> 1
        states = []
        actuation_types = []
        for loc in self.solenoids:
            val = int_data & 0b11
            actuation = self.get_actuation_type(val)
            actuation_types.append(actuation)
#            print(val, actuation)
            states.append(SolenoidState.CLOSED if actuation == ActuationType.CLOSE_VENT or actuation == ActuationType.NONE else SolenoidState.OPEN)
            int_data = int_data >> 2

        for idx in range(self.num_solenoids):
            valve_loc = self.solenoids[idx]
            self.registry.put(("valve", ValveType.SOLENOID, valve_loc), states[idx])
            self.registry.put(("valve_actuation", "actuation_type", ValveType.SOLENOID, valve_loc), actuation_types[idx])


    def actuate_solenoids(self):
        for loc in self.solenoids:
            _, actuation_type = self.flag.get(("solenoid", "actuation_type", loc))
            _, actuation_priority = self.flag.get(("solenoid", "actuation_priority", loc))
            if actuation_priority != ValvePriority.NONE:
                _, curr_priority, _ = self.registry.get(("valve_actuation", "actuation_priority", ValveType.SOLENOID, loc))
#                print(actuation_priority, curr_priority)
                if actuation_priority >= curr_priority:
                    if actuation_type == ActuationType.NONE:
                        print("Allowing others to actuate")
                        command = self.get_command(loc, ActuationType.CLOSE_VENT)
                        self.registry.put(("valve_actuation", "actuation_type", ValveType.SOLENOID, loc), actuation_type)
                        self.registry.put(("valve_actuation", "actuation_priority", ValveType.SOLENOID, loc), ValvePriority.NONE)
                    else:
                        print("Actuating")
                        command = self.get_command(loc, actuation_type)
                        self.registry.put(("valve_actuation", "actuation_type", ValveType.SOLENOID, loc), actuation_type)
                        self.registry.put(("valve_actuation", "actuation_priority", ValveType.SOLENOID, loc), actuation_priority)

                    self.arduino.write(command)
                    self.flag.put(("solenoid", "actuation_type", loc), ActuationType.NONE)
                    self.flag.put(("solenoid", "actuation_priority", loc), ValvePriority.NONE)



    #TODO: Fix the structure of this method, it's completely different from other classes and won't work properly
    def actuate(self):
#        if self.registry.get(("general", "soft_abort"))[1] or self.registry.get(("general", "hard_abort"))[1]:
            # Can't actuate if the rocket's been aborted
#            return
        self.actuate_solenoids()
