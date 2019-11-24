import sys
import time

#python3 sensors_test.py thermo 50 .1

name = sys.argv[1]
iterations = int(sys.argv[2])
delay = float(sys.argv[3])

if name == "thermo":
    import Adafruit_GPIO
    from Adafruit_MAX31856 import MAX31856 as MAX31856
    port, device = 0, 0
    sensor = MAX31856(hardware_spi=Adafruit_GPIO.SPI.SpiDev(port, device), tc_type=MAX31856.MAX31856_K_TYPE)
    for i in range(iterations):
        print("Temperature:", sensor.read_temp_c())
        print("Internal:", sensor.read_internal_temp_c())
        time.sleep(delay)
elif name == "imu":
    pass
elif name == "load":
    import RPi.GPIO as GPIO
    sck, dat = 5, 6
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sck, GPIO.OUT)
    for j in range(iterations):
        i = 0
        count = 0
        GPIO.setup(dat, GPIO.OUT)
        GPIO.output(dat, 1)
        GPIO.output(sck, 0)
        GPIO.setup(dat, GPIO.IN)

        while GPIO.input(dat) == 1:
            i = 0

        # Calculates the kg value of the load cell using the clock and reading from the data pin
        for i in range(24):
            GPIO.output(sck, 1)
            count = count << 1

            GPIO.output(sck, 0)
            time.sleep(0.001)
            if GPIO.input(dat) == 0:  # HX711 values are in 2s complement
                count = count + 1

        GPIO.output(sck, 1)
        count = count ^ 0x800000  # clear 24th bit
        GPIO.output(sck, 0)

        # Calibration
        weight = (9584000 - count) / 845165
        print("Weight:", weight)
        time.sleep(delay)