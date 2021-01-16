import json
import time
import random
import struct
import threading
from modules.drivers.driver import Driver
from modules.lib.enums import ActuationType, ValveType, SolenoidState, SensorType

PULSE_TIMER = 0.5
SPECIAL_VENT_TIMER = 4
RELIEF_TIMER = 1

class PseudoSensor():
    def __init__(self, config: dict, registry: dict):
        print("CREATING PSEUDO SENSOR")
        self.has_written = False
        self.registry = registry
        self.config = config
        self.sensor_config = config["list"]
        self.sensor_list = [(s_type, loc) for s_type in self.sensor_config for loc in self.sensor_config[s_type]]
        self.num_sensors = len(self.sensor_list)
        self.sensors = {i: random.randint(100, 200) for i in self.sensor_list}
        self.read_queue = []
        self.ranges = json.load(open("modules/drivers/pseudo_sensor_ranges.json"))["ranges"]


    def set_sensor_values(self):
        curr_stage = self.registry.get(("general", "stage"))[1]
        for sensor in self.ranges:
            for loc in self.ranges[sensor]:
                current_range = self.ranges[sensor][loc][curr_stage]
                # assert((sensor, loc) in self.sensors)
                if (sensor, loc) in self.sensors:
                    self.sensors[(sensor, loc)] = random.randint(current_range[0], current_range[1])
#        self.sensors = {i: self.sensors[i] + random.randint(-10, 10) for i in self.sensor_list}


    def register_sensors(self, msg):
        num_sensors, num_thermos, num_pressures = msg[0], msg[1], msg[2]
        assert(num_sensors == self.num_sensors and num_thermos + num_pressures == num_sensors)
        idx = 3
        self.pins, self.inv_pins = {}, {}
        while idx < len(msg):
            if msg[idx] == 1:
                pin = msg[idx + 1]
                for loc in self.sensor_config[SensorType.PRESSURE]:
                    if self.sensor_config[SensorType.PRESSURE][loc]["pin"] == pin:
                        self.pins[pin] = (SensorType.PRESSURE, loc)
                        self.inv_pins[(SensorType.PRESSURE, loc)] = pin
                idx += 2
            elif msg[idx] == 0:
                pin = msg[idx + 1]
                pins = [msg[idx + i] for i in range(1, 5)]
                for loc in self.sensor_config[SensorType.THERMOCOUPLE]:
                    if self.sensor_config[SensorType.THERMOCOUPLE][loc]["pins"] == pins:
                        self.pins[pins[0]] = (SensorType.THERMOCOUPLE, loc)
                        self.inv_pins[(SensorType.THERMOCOUPLE, loc)] = pins[0]
                idx += 5
            else:
                raise Exception("Unknown sensor being registered in PseudoSensor")
        assert(len(self.pins) == len(self.inv_pins) == self.num_sensors)
        self.read_queue.append(255)


    def read(self, num_bytes):
        if self.read_queue:
            sub = self.read_queue[:num_bytes]
            self.read_queue = self.read_queue[num_bytes:]
            return bytes(sub)
        self.set_sensor_values()
        ret = bytes()
        for key in self.sensors:
            ret += bytes([self.inv_pins[key]])
            ret += struct.pack('f', self.sensors[key])
        assert(len(ret) == self.num_sensors * 5)
        return ret
    

    def write(self, msg):
        if not self.has_written: # Only register sensors on the first message that is recieved
            self.register_sensors(msg)
            self.has_written = True


class PseudoSolenoid():

    def __init__(self, pin: int, isSpecial: bool, isNO: bool):
        self.pin = pin
        self.isSpecial = isSpecial
        self.isNO = isNO
        self.resting = SolenoidState.OPEN if isNO else SolenoidState.CLOSED
        self.state = self.resting
        self.actuation = ActuationType.NONE
        self.command = 0
    

    def get_data(self):
        return bytes([self.pin, self.state.value, self.actuation.value])


    def open_vent(self):
        self.state = SolenoidState.OPEN
        self.actuation = ActuationType.OPEN_VENT
        if not self.isNO and self.isSpecial:
            thread = threading.Thread(target=self.relief_thread, args=(SolenoidState.OPEN, SolenoidState.CLOSED, self.command))
            thread.daemon = True
            thread.start()        

    
    def close_vent(self):
        self.state = SolenoidState.CLOSED
        self.actuation = ActuationType.CLOSE_VENT
        if self.isNO and self.isSpecial:
            thread = threading.Thread(target=self.relief_thread, args=(SolenoidState.CLOSED, SolenoidState.OPEN, self.command))
            thread.daemon = True
            thread.start()        


    def relief_thread(self, current_state, relief_state, cmd):
        relieving = False
        while True:
            if cmd != self.command:
                return
            if relieving:
                self.state = relief_state
                time.sleep(RELIEF_TIMER)
            else:
                self.state = current_state
                time.sleep(SPECIAL_VENT_TIMER)
            relieving = not relieving


    def pulse_thread(self, cmd):
        self.state = SolenoidState.OPEN
        self.actuation = ActuationType.PULSE
        time.sleep(PULSE_TIMER)
        if self.command != cmd:
            return
        self.state = SolenoidState.CLOSED
        self.actuation = ActuationType.NONE


    def actuate(self, actuation_type):
        self.command += 1
        if actuation_type == ActuationType.OPEN_VENT:
            self.open_vent()
        elif actuation_type == ActuationType.CLOSE_VENT:
            self.close_vent()
        elif actuation_type == ActuationType.NONE:
            if self.actuation == ActuationType.PULSE: # Kill the pulse, return to closed state
                self.close_vent()
            self.actuation = ActuationType.NONE
        elif actuation_type == ActuationType.PULSE:
            thread = threading.Thread(target=self.pulse_thread, args=(self.command,))
            thread.daemon = True
            thread.start()


class PseudoValve():
    def __init__(self, config: dict, registry: dict):
        print("CREATING PSEUDO VALVE")
        self.registry = registry
        self.config = config
        self.valve_config = self.config["list"]
        print(self.valve_config)
        self.solenoid_locs = [loc for loc in self.valve_config[ValveType.SOLENOID]]
        self.num_solenoids = len(self.solenoid_locs)
        
        self.has_written = False
        self.pins, self.solenoids = {}, []
        self.read_queue = []


    def read(self, num_bytes):
        if self.read_queue:
            sub = self.read_queue[:num_bytes]
            self.read_queue = self.read_queue[num_bytes:]
            return bytes(sub)
        assert(num_bytes == self.num_solenoids * 3)
        to_ret = bytes()
        for solenoid in self.solenoids:
            to_ret += solenoid.get_data()
        return to_ret
    

    def write_actuation(self, msg):
        # Message structure: [loc, actuation type]
        # print("Got actuation msg:", msg)
        pin = msg[0]
        actuation_int = msg[1]
        solenoid = self.pins[pin]
        actuation_type = ActuationType(actuation_int)
        solenoid.actuate(actuation_type)


    def find_loc(self, pin):
        for loc in self.valve_config[ValveType.SOLENOID]:
            if self.valve_config[ValveType.SOLENOID][loc]["pin"] == pin:
                return loc
        assert(False)


    def register_solenoids(self, msg):
        assert(self.num_solenoids == msg[0])
        assert(len(msg) == self.num_solenoids * 3 + 1)
        idx = 1
        while idx < len(msg):
            pin = msg[idx]
            isSpecial = bool(msg[idx + 1])
            isNO = bool(msg[idx + 2])
            loc = self.find_loc(pin)
            sol = PseudoSolenoid(pin, isSpecial, isNO)
            self.solenoids.append(sol)
            self.pins[pin] = sol
            idx += 3

        assert(len(self.pins) == len(self.solenoids) == self.num_solenoids)
        self.read_queue.append(253)


    def write(self, msg):
        if not self.has_written: # Only register sensors on the first message that is recieved
            self.register_solenoids(msg)
            self.has_written = True
            return
        
        if msg[0] == 254:
            self.write_actuation(msg[1:])
    

class Arduino(Driver):

    def __init__(self, name: "str", config: dict, registry: dict):
        super().__init__(name)
        self.name = name
        print("MY NAME IS", self.name)
        self.registry = registry
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
        if self.name == "sensor_arduino":
            self.arduino = PseudoSensor(self.config, self.registry)
        else:
            self.arduino = PseudoValve(self.config, self.registry)

    """
    Read data from the Arduino and return it
    Ex. [10, 20, 0, 0, 15, 0, 0, 0, 14, 12, 74, 129]
    """
    def read(self, num_bytes: int) -> bytes:
        return self.arduino.read(num_bytes)

    """
    Write data to the Arduino and return True if the write was successful else False
    """
    def write(self, msg: bytes) -> bool:
        self.arduino.write(msg)
    