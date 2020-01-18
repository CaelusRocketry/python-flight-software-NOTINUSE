# /modules/solenoid

import time
from aenum import Enum, auto
from time import sleep
from multiprocessing import Process

# Local Imports
from . import Valve, ValveType

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

# Position
CLOSE = 0
OPEN = 90


class Solenoid(Valve):
    def __init__(self, id, valve_type, dir, pin, gear_ratio=GEAR_RATIO, delay=DELAY_TIME):
        self.postition = CLOSE
        super(id, ValveType.Vent, pin, gear_ratio) # id, valve_type, pin, gear_ratio

    def setup(self):
        if REAL:
             GPIO.setmode(GPIO.BCM)
             GPIO.setup(self.pin, GPIO.OUT)

    def abort(self):
         self.actuate(OPEN, ABORT_PRIORITY) 

    # def _step excluded

    def start_vent(self):
        self.is_venting = True
        self.actuate(OPEN, VENT_PRIORITY)

    def stop_vent(self):
        if self.is_venting == True:
            self.is_venting = False
            self.actuate(CLOSE, VENT_PRIORITY)

    def pulse(self):
        for x in range(5):
            self.actuate(CLOSE, PULSE_PRIORITY)
            time.sleep(0.5)
            self.actuate(OPEN, PULSE_PRIORITY)
            time.sleep(0.5)
    
    def purge(self, priority):
        self.actuate(CLOSE, PURGE_PRIORITY)


    def goto(self, target):
        if target != self.angle:    
            if target == OPEN: 
                GPIO.output(self.pin, HIGH)
            else target == CLOSE:
                GPIO.output(self.pin, LOW)
            self.is_actuating = False
            self.interrupt = False


    def actuate(self, target, priority):
        print("Switching solenoid", self.id, target, priority)
        if self.is_actuating:
            if priority >= self.priority:
                print("Interrupting")
                self.interrupt = True
                while self.is_actuating:
                    pass
                self.priority = priority
                self.goto(target)
            else:
                print("Not actuating, command is lower priority")
        else:
            self.priority = priority
            self.goto(target)



