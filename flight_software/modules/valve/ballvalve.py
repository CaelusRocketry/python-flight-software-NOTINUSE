# /modules/ballvalve

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

class BallValve(Valve):
    def __init__(self, id, dir, pin, gear_ratio=GEAR_RATIO, delay=DELAY_TIME):
        self.dir = dir
        self.delay = delay
        self.angle = 0
        super(id, ValveType.Ball, pin, gear_ratio) # id, valve_type, pin, gear_ratio

    def setup(self):
        if REAL:
             GPIO.setmode(GPIO.BCM)
             GPIO.setup(self.dir, GPIO.OUT)
             GPIO.setup(self.pin, GPIO.OUT)
    
    def abort(self):
        self.actuate(0, ABORT_PRIORITY)  # emptying

    def _step(self):
        GPIO.output(self.pin, HIGH)
        sleep(self.delay)
        GPIO.output(self.pin, LOW)
        sleep(self.delay)

    def goto(self, target):
        print("Going to", self.angle, target)
        start = time.time()
        angle = target - self.angle
        angle %= 360
        if angle > 180:
            angle = angle - 360
        steps = int(self.full * self.gear_ratio * angle / 360)

        GPIO.output(self.dir, HIGH)
        if steps < 0:
            GPIO.output(self.dir, LOW)
            steps *= -1

        #print(target, self.angle, steps * direction)

        self.interrupt = False
        self.is_actuating = True
        start = time.time()
        for i in range(steps):
            self._step()
            self.angle += angle / steps
            if self.interrupt:
                print("Interrupting actuation for some reason")
                break
        self.priority = -1
        self.is_actuating = False
        self.interrupt = False
        print("Done actuating")
        print("Took", str(time.time() - start), "seconds to actuate")

    def start_vent(self):
        self.is_venting = True
        self.actuate(0, VENT_PRIORITY)

    def stop_vent(self):
        if self.is_venting == True:
            self.is_venting = False
            self.actuate(90, VENT_PRIORITY)

    def pulse(self):
        for x in range(5):
            self.actuate(90, PULSE_PRIORITY)
            time.sleep(0.5)
            self.actuate(0, PULSE_PRIORITY)
            time.sleep(0.5)
    
    def purge(self, priority):
        self.actuate(90, PURGE_PRIORITY)

    def actuate(self, target, priority):
        print("Started actuation thread")
        actuate_thread = Process(target=self._actuate, args=(target, priority))
        actuate_thread.daemon = True
        actuate_thread.start()
        actuate_thread.join()

    def _actuate(self, target, priority):
        print("Actuating", self.id, target, priority)
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
