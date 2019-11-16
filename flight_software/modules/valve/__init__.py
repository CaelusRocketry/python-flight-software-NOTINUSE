# /modules/valve

import time
from aenum import Enum, auto
from time import sleep
from multiprocessing import Process

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

class Valve:
    def __init__(self, id, valve_type, dir, step,
                 gear_ratio=GEAR_RATIO, delay=DELAY_TIME):
        self.id = id
        self.type = valve_type
        self.is_actuating = False
        self.gear_ratio = gear_ratio
        self.dir = dir
        self.step = step
        self.active = False
        self.aborted = False
        self.delay = delay
        self.angle = 0
        self.full = 200
        self.priority = -1
        self.setup()

    def setup(self):
        if REAL:
             GPIO.setmode(GPIO.BCM)
             GPIO.setup(self.dir, GPIO.OUT)
             GPIO.setup(self.step, GPIO.OUT)

    def abort(self):
        if self.type == Valve.Ball:
            self.actuate(0, ABORT_PRIORITY)  # emptying
        else:
            self.actuate(90, ABORT_PRIORITY)  # ep

    def _step(self):
        GPIO.output(self.step, HIGH)
        sleep(self.delay)
        GPIO.output(self.step, LOW)
        sleep(self.delay)

    def goto(self, target):
        print("Going to", self.angle, target)
        start = time.time()
        angle = target - self.angle
        angle %= 360
        if angle > 180:
            angle = angle - 360
        steps = int(self.full * self.gear_ratio * angle / 360)
        direction = 1
        GPIO.output(self.dir, HIGH)
        if steps < 0:
            direction = -1
            GPIO.output(self.dir, LOW)
            steps *= -1

#        print(target, self.angle, steps * direction)

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
        if self.type == Valve.Ball:
            self.actuate(0, VENT_PRIORITY)
        else:
            self.actuate(90, VENT_PRIORITY)

    def stop_vent(self):
        if self.is_venting == True:
            self.is_venting = False
            if self.type == Valve.Ball:
                self.actuate(90, VENT_PRIORITY)
            else:
                self.actuate(0, VENT_PRIORITY)

    def pulse(self):
        if self.type == Valve.Ball:
            for x in range(5):
                self.actuate(90, PULSE_PRIORITY)
                time.sleep(0.5)
                self.actuate(0, PULSE_PRIORITY)
                time.sleep(0.5)
        else:
            for x in range(5):
                self.actuate(0, PULSE_PRIORITY)
                time.sleep(0.5)
                self.actuate(90, PULSE_PRIORITY)
                time.sleep(0.5)

    def purge(self, priority):
        if self.type == Valve.Ball:
            self.actuate(90, PURGE_PRIORITY)
        else:
            self.actuate(0, PURGE_PRIORITY)

    def actuate(self, target, priority):
        print("Started actuation thread")
        actuate_thread = Process(target=self._actuate, args=(target, priority))
        actuate_thread.daemon = True
        actuate_thread.start()
        actuate_thread.join()

    def _actuate(self, target, priority):
        print("Actuating", self.id, target, priority)
        if self.aborted:
            return
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


def indefinite(direction):
    valve = Valve(0, ValveType.Ball, 4, 17)
    if direction:
        GPIO.output(valve.dir, HIGH)
    else:
        GPIO.output(valve.dir, HIGH)
    while True:
        valve._step()


if __name__ == '__main__':
    indefinite(True)

""" if __name__ == '__main__':
    valve = Valve(0, ValveType.Ball, 4, 17)
    while 1:
        x = input()
        if x == "x":
            break
        degree, priority = [int(i) for i in x.split(" ")]
        actuate_thread = threading.Thread(
            target=valve.actuate, args=(degree, priority))
        actuate_thread.daemon = True
        actuate_thread.start()
    valve.abort() """

