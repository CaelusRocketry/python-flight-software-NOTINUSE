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
        self.sensors = {i: random.random() * 50 for i in self.sensor_list}


    def set_sensor_values(self):
        self.sensors = {i: self.sensors[i] + random.randint(-5, 5) for i in self.sensor_list}


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
        self.actuation_types = list(ActuationType)
        self.solenoid_locs = [loc for loc in valves[ValveType.SOLENOID]]
        self.valve_states = {(ValveType.SOLENOID, loc): SolenoidState.CLOSED for loc in self.solenoid_locs}
        self.valve_actuations = {(ValveType.SOLENOID, loc): ActuationType.NONE for loc in self.solenoid_locs}


    def read(self):
#        self.set_sensor_values()
        state_dict = {SolenoidState.OPEN: 0, SolenoidState.CLOSED: 1}
        actuation_dict = {ActuationType.PULSE: 0, ActuationType.OPEN_VENT: 1, ActuationType.CLOSE_VENT: 2, ActuationType.NONE: 3}
        ret = []
        for key in self.valve_states:
            ret.append(state_dict[self.valve_states[key]])
            ret.append(actuation_dict[self.valve_actuations[key]])
        return bytes(ret)
    

    def actuate(self, valve, state1, timer, state2):
        self.valve_states[valve] = state1
        time.sleep(timer)
        self.valve_states[valve] = state2
        self.valve_actuations[valve] = ActuationType.NONE


    def write(self, msg):
        #Formula: idx1 * 16 + idx2
        loc_idx = msg // 16
        actuation_idx = msg % 16
        valve = (ValveType.SOLENOID, self.solenoid_locs[loc_idx])
        actuation_type = self.actuation_types[actuation_idx]
        # Switch statement
        if actuation_type == ActuationType.NONE:
            # Reset
            raise NotImplementedError
        elif actuation_type == ActuationType.OPEN_VENT:
            state1 = SolenoidState.OPEN
            timer = 0
            state2 = SolenoidState.OPEN
        elif actuation_type == ActuationType.CLOSE_VENT:
            state1 = SolenoidState.CLOSED
            timer = 0
            state2 = SolenoidState.CLOSED
        elif actuation_type == ActuationType.PULSE:
            print("Pulsing")
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
    