from modules.tasks.task import Task
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.lib.enums import ValveType, SolenoidState, ActuationType, ValvePriority
import struct
from enum import Enum, auto

SEND_DATA_CMD = 255
ACTUATE_CMD = 254
CONFIRMATION = 253

class ValveTask(Task):
    def __init__(self, registry: Registry, flag: Flag):
        self.name = "Valve Arduino"
        self.registry = registry
        self.flag = flag

    def begin(self, config):
        #TODO: fix this, it's really hacky and just a temporary workaround (let's see how long it stays though)
        if config["arduino_type"] == "pseudo":
            from modules.drivers.pseudo_arduino import Arduino
        else:
            from modules.drivers.real_arduino import Arduino

        self.config = config["valves"]
        #TODO: Make sure that this is the same order that the arduino returns its data in
        self.valve_config = self.config["list"]
        self.solenoids = [loc for loc in self.valve_config[ValveType.SOLENOID]]
        self.num_solenoids = len(self.solenoids)
        self.arduino = Arduino(self.name, self.config)
        self.pins, self.inv_pins = {}, {}
        self.send_valve_info()
    

    def send_valve_info(self):
        to_send = [len(self.solenoids)]
        for valve_type in self.valve_config:
            for loc in self.valve_config[valve_type]:
                temp = self.valve_config[valve_type][loc]
                to_send.append(temp["pin"])
                to_send.append(1 if temp["special"] else 0)
                to_send.append(1 if temp["natural"] == "OPEN" else 0)
                self.pins[temp["pin"]] = (ValveType.SOLENOID, loc)
                self.inv_pins[(ValveType.SOLENOID, loc)] = temp["pin"]
        print("Sending valve info:", to_send)
        self.arduino.write(bytes(to_send))
        assert(self.arduino.read(1) == bytes([CONFIRMATION]))


    def get_float(self, data):
        byte_array = bytes(data)
        return struct.unpack('f', byte_array)[0]


    def get_command(self, loc, actuation_type):
        # Message structure: [pin, actuation type]
        pin = self.inv_pins[(ValveType.SOLENOID, loc)]
        return [ACTUATE_CMD, pin, actuation_type.value]


    def read(self):
        # print("Reading valve data")
        self.arduino.write([SEND_DATA_CMD])
        byte_data = self.arduino.read(self.num_solenoids * 3)
        for i in range(self.num_solenoids):
            solenoid_data = byte_data[i*3:(i + 1)*3]

#            print("pin", solenoid_data[0])
#            print("state", solenoid_data[1])
#            print("actuation", solenoid_data[2])

            
            pin = solenoid_data[0]
            state = SolenoidState(solenoid_data[1])
            actuation = ActuationType(solenoid_data[2])
            valve_type, loc = self.pins[pin]
            self.registry.put(("valve", valve_type, loc), state)
            self.registry.put(("valve_actuation", "actuation_type", valve_type, loc), actuation)


    def actuate_solenoids(self):
        for loc in self.solenoids:
            _, actuation_type = self.flag.get(("solenoid", "actuation_type", loc))
            _, actuation_priority = self.flag.get(("solenoid", "actuation_priority", loc))
            _, curr_priority, _ = self.registry.get(("valve_actuation", "actuation_priority", ValveType.SOLENOID, loc))
            if actuation_priority != ValvePriority.NONE and actuation_priority <= curr_priority:
                print("Actuating", loc, actuation_type, actuation_priority)
                if actuation_type == ActuationType.NONE:
                    actuation_priority = ValvePriority.NONE
                self.registry.put(("valve_actuation", "actuation_type", ValveType.SOLENOID, loc), actuation_type)
                self.registry.put(("valve_actuation", "actuation_priority", ValveType.SOLENOID, loc), actuation_priority)

                command = self.get_command(loc, actuation_type)
                # print("Sending actuation message:", command)
                self.arduino.write(command)

                self.flag.put(("solenoid", "actuation_type", loc), ActuationType.NONE)
                self.flag.put(("solenoid", "actuation_priority", loc), ValvePriority.NONE)


    def actuate(self):
        self.actuate_solenoids()
