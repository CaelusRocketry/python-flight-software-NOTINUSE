import RPi.GPIO as GPIO
from RPi.GPIO import HIGH, LOW
from time import sleep
import threading
import time

GEAR_RATIO = 50
DELAY_TIME = .001


class Valve:

    def __init__(self, dir, step, gear_ratio=GEAR_RATIO, delay=DELAY_TIME):
        self.is_acuating = False
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
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir, GPIO.OUT)
        GPIO.setup(self.step, GPIO.OUT)

    def abort(self):
        GPIO.output(self.step, LOW)
        GPIO.cleanup()
        self.aborted = True

    def _step(self):
        GPIO.output(self.step, HIGH)
        sleep(self.delay)
        GPIO.output(self.step, LOW)
        sleep(self.delay)

    def goto(self, target):
        print(self.angle, target)
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

        print(target, self.angle, steps*direction)

        self.interrupt = False
        self.is_acuating = True
        for i in range(steps):
            self._step()
            self.angle += angle / steps
            if self.interrupt:
                print("Interrupting actuation for some reason")
                break
        self.priority = -1
        self.is_acuating = False
        self.interrupt = False
        print("Done actuating")

    def actuate(self, target, priority):
        print(target, priority)
        if self.aborted:
            return
        if self.is_acuating:
            if priority >= self.priority:
                print("Interrupting")
                self.interrupt = True
                while self.is_acuating:
                    pass
                self.priority = priority
                self.goto(target)
            else:
                print("Not actuating, command is lower priority")
        else:
            self.priority = priority
            self.goto(target)


if __name__ == '__main__':
    valve = Valve(4, 17)
    while 1:
        x = input()
        if x == "x":
            break
        degree, priority = [int(i) for i in x.split(" ")]
        actuate_thread = threading.Thread(
            target=valve.actuate, args=(degree, priority))
        actuate_thread.daemon = True
        actuate_thread.start()

    valve.abort()
