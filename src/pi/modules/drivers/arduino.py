import json
import time
import random
import struct
import threading
from modules.drivers.driver import Driver
from modules.lib.enums import ActuationType, ValveType, SolenoidState
"""
Pseudo arduino class to use to run code on ur own laptop!
FIXME: The real_arduino.py class should be used on the pi!
"""
class PseudoSensor():
    def __init__(self, config: dict):
        print("CREATING PSEUDO SENSOR")
        self.config = config
        sensors = config["list"]
        self.sensor_list = [(s_type, loc) for s_type in sensors for loc in sensors[s_type]]
        self.num_sensors = len(self.sensor_list)
        self.sensors = {i: random.randint(100, 200) for i in self.sensor_list}


    def set_sensor_values(self):
        import os
        print("Waiting")
        time.sleep(0.7)
        ranges = json.load(open("modules/drivers/pseudo_sensor_ranges.json"))["ranges"]
        for sensor in ranges:
            for loc in ranges[sensor]:
                range = ranges[sensor][loc]
                assert((sensor, loc) in self.sensors)
                self.sensors[(sensor, loc)] = random.randint(range[0], range[1])
#        self.sensors = {i: self.sensors[i] + random.randint(-10, 10) for i in self.sensor_list}


    def read(self):
        self.set_sensor_values()
        ret = bytes()
        for key in self.sensors:
            ret += struct.pack('f', self.sensors[key])
        return ret
    
    def write(self, msg):
        pass


class PseudoValve():
    def __init__(self, config: dict):
        print("CREATING PSEUDO VALVE")
        self.config = config
        valves = self.config["list"]
        self.solenoid_locs = [loc for loc in valves[ValveType.SOLENOID]]
        self.valve_states = {(ValveType.SOLENOID, loc): SolenoidState.CLOSED for loc in self.solenoid_locs}
        self.valve_actuations = {(ValveType.SOLENOID, loc): ActuationType.NONE for loc in self.solenoid_locs}
        self.state_dict = {SolenoidState.CLOSED: 0, SolenoidState.OPEN: 1}
        self.actuation_dict = {ActuationType.NONE: 0, ActuationType.CLOSE_VENT: 1, ActuationType.OPEN_VENT: 2, ActuationType.PULSE: 3}
        self.inv_actuations = {self.actuation_dict[k]:k for k in self.actuation_dict}


    def read(self):
#        print(self.valve_actuations)
#        print(self.valve_states.values(), self.valve_actuations.values())
#        time.sleep(0.5)
        data = 0
        for idx, loc in enumerate(self.solenoid_locs):
            state = self.actuation_dict[self.valve_actuations[(ValveType.SOLENOID, loc)]]
            data = data | (state << (idx * 2 + 1))
        return int.to_bytes(data, 4, 'big')
    

    def actuate(self, valve, state1, timer, state2):
        self.valve_states[valve] = state1
        if timer != -1:
            time.sleep(timer)
        self.valve_states[valve] = state2
        print("Done actuating boi")
        if timer != -1:
            print("Setting valve actuation type to none")
            self.valve_actuations[valve] = ActuationType.NONE


    def write(self, msg):
        # Message structure: [loc, actuation type]
        loc_idx = msg[0]
        actuation_idx = msg[1]
        valve = (ValveType.SOLENOID, self.solenoid_locs[loc_idx])
        actuation_type = self.inv_actuations[actuation_idx]
#        print("Actuating:", valve, actuation_type)
        # Switch statement
        if actuation_type == ActuationType.OPEN_VENT:
            state1 = SolenoidState.OPEN
            timer = -1
            state2 = SolenoidState.OPEN
        elif actuation_type == ActuationType.CLOSE_VENT or actuation_type == ActuationType.NONE:
            state1 = SolenoidState.CLOSED
            timer = -1
            state2 = SolenoidState.CLOSED
        elif actuation_type == ActuationType.PULSE:
            state1 = SolenoidState.OPEN
            #TODO: Change the timer to the actual pulse timer
            timer = 2.0
            state2 = SolenoidState.CLOSED

        self.valve_actuations[valve] = actuation_type
        thread = threading.Thread(target=self.actuate, args=(valve, state1, timer, state2))
        thread.daemon = True
        thread.start()


class Arduino(Driver):

    def __init__(self, name: "str", config: dict):
        super().__init__(name)
        self.name = name
        print("MY NAME IS")
        print(self.name)
        self.config = config
        self.address = self.config["address"]
        self.reset()
    
    """
    Return whether or not the i2c connection is alive
    """
    def status(self) -> bool:
        # ping = "hey u alive"
        # ping_bytes = [ord(b) for b in ping]
        # self.write(ping_bytes)

        # time.sleep(.3)

        # response = self.read()
        # return struct.unpack('f', response)[0] == "yeah i'm good"
        pass

    """
    Powercycle the arduino
    """
    def reset(self) -> bool:
        if self.name == "Sensor Arduino":
            self.arduino = PseudoSensor(self.config)
        else:
            self.arduino = PseudoValve(self.config)

    """
    Read data from the Arduino and return it
    Ex. [10, 20, 0, 0, 15, 0, 0, 0, 14, 12, 74, 129]
    """
    def read(self, num_bytes: int) -> bytes:
        return self.arduino.read()

    """
    Write data to the Arduino and return True if the write was successful else False
    """
    def write(self, msg: bytes) -> bool:
        self.arduino.write(msg)
    