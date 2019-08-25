import RPi.GPIO as GPIO
from RPi.GPIO import HIGH, LOW
import time 

GEAR_RATIO = 50
HALF_STEP = False
DELAY_TIME = (1/2 if HALF_STEP else 1)*0.001

out1 = 13
out2 = 11
out3 = 15
out4 = 12

half_step_dict = {
    -1: [LOW, LOW, LOW, LOW],
    0: [HIGH, LOW, LOW, LOW],
    1: [HIGH, HIGH, LOW, LOW],
    2: [LOW, HIGH, LOW, LOW],
    3: [LOW, HIGH, HIGH, LOW],
    4: [LOW, LOW, HIGH, LOW],
    5: [LOW, LOW, HIGH, HIGH],
    6: [LOW, LOW, LOW, HIGH],
    7: [HIGH, LOW, LOW, HIGH]
}

full_step_dict = {
    -1: [LOW, LOW, LOW, LOW],
    0: [HIGH, LOW, LOW, HIGH],
    1: [LOW, HIGH, LOW, HIGH],
    2: [LOW, HIGH, HIGH, LOW],
    3: [HIGH, LOW, HIGH, LOW]
}

class Valve:
    
    def __init__(self, out1, out2, out3, out4):
        self.out1 = out1
        self.out2 = out2
        self.out3 = out3
        self.out4 = out4
        self.angle = 0
        self.step_num = 0

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(out1,GPIO.OUT)
        GPIO.setup(out2,GPIO.OUT)
        GPIO.setup(out3,GPIO.OUT)
        GPIO.setup(out4,GPIO.OUT)

    def step(self, i):
        stepper_dict = half_step_dict if HALF_STEP else full_step_dict
        GPIO.output(self.out1,stepper_dict[i][0])
        GPIO.output(self.out2,stepper_dict[i][1])
        GPIO.output(self.out3,stepper_dict[i][2])
        GPIO.output(self.out4,stepper_dict[i][3])

#Angle in degrees
    def setPos(self, target):
        try:
            start = time.time()
            self.step(-1)
            angle = target - self.angle
            angle %= 360
            if angle > 180:
                angle = angle - 360
            steps_per_rotation = 400 if HALF_STEP else 200
            steps = steps_per_rotation * GEAR_RATIO * angle / 360
            diff = 1
            if steps < 0:
                steps = -steps
                diff = -1
                
            print(angle, self.angle, steps*diff)
            for y in range(steps):
                self.step(self.step_num)
                time.sleep(DELAY_TIME)
                self.step_num += diff
                if HALF_STEP:
                    if self.step_num == -1: self.step_num = 7
                    if self.step_num == 8: self.step_num = 0
                else:
                    if self.step_num == -1: self.step_num = 3
                    if self.step_num == 4: self.step_num = 0
                if y % steps_per_rotation == 0:
                    self.step(-1)
            self.angle = target
            print("Done")
        except KeyboardInterrupt:
            GPIO.cleanup()

valve = Valve(out1, out2, out3, out4)
while 1:
    x = input()
    valve.setPos(int(x))