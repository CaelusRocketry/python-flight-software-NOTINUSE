# /modules/valve

import time
from aenum import Enum, auto
from time import sleep
from multiprocessing import Process
from abc import ABC, abstractmethod

try:
    import RPi.GPIO as GPIO
    from RPi.GPIO import HIGH, LOW
except:
    print("Skipping GPIO on non-pi...")
    REAL = False
else:
    print("Loaded GPIO")
    REAL = True

GEAR_RATIO = 50
DELAY_TIME = .001

# change later
ABORT_PRIORITY = 10
PURGE_PRIORITY = 9
PULSE_PRIORITY = 8
VENT_PRIORITY = 7

class ValveType(Enum):
    Ball = auto()
    Vent = auto()
    Drain = auto() 

class Valve(ABC):

    def __init__(self, id, valve_type, pin, gear_ratio=GEAR_RATIO):
        self.id = id
        self.type = valve_type
        self.is_actuating = False
        self.gear_ratio = gear_ratio
        self.pin = pin
        self.active = False
        self.full = 200
        self.priority = -1
        self.setup()


    @abstractmethod
    def setup(self):
        pass


    @abstractmethod
    def abort(self):
        pass

    @abstractmethod
    def start_vent(self):
        pass

    @abstractmethod
    def stop_vent(self):
        pass

    @abstractmethod
    def pulse(self):
        pass

    @abstractmethod
    def purge(self):
        pass

    @abstractmethod
    def actuate(self):
        pass

    @abstractmethod
    def goto(self):
        pass



def indefinite(direction):
    import time
    valve = BallValve(0, ValveType.Ball, 4, 17)
    if direction:
        GPIO.output(valve.dir, LOW)
    else:
        GPIO.output(valve.dir, HIGH)
    while True:
        print("HI")
        valve._step()
        time.sleep(0.04)