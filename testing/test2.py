import RPi.GPIO as gpio
import time

DT = 5
SCK = 6

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(SCK, gpio.OUT)


def readCount():
    i = 0
    Count = 0
    gpio.setup(DT, gpio.OUT)
    gpio.output(DT, 1)
    gpio.output(SCK, 0)
    gpio.setup(DT, gpio.IN)

    while gpio.input(DT) == 1:
        i = 0

    for i in range(24):
        gpio.output(SCK, 1)
        Count = Count << 1

        gpio.output(SCK, 0)
        time.sleep(0.001)
        if gpio.input(DT) == 0:  # HX711 values are in 2s complement
            Count = Count + 1

    gpio.output(SCK, 1)
    Count = Count ^ 0x800000  # clear 24th bit
    gpio.output(SCK, 0)
    # Calibration
    Count = (9584000 - Count) / 845165
    return Count


while True:
    count = readCount()
    print(count)
    time.sleep(.2)
