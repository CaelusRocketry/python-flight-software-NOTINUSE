# Make sure to pip3 install adafruit-circuitpython-max31865

import board
import busio
import time
import digitalio
import adafruit_max31865

# Initialize SPI bus and sensor
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)  # Chip select/chip enable
sensor = adafruit_max31865.MAX31865(spi, cs)

if __name__ == "__main__":
    while True:
        temp = sensor.temperature
        print('Temperature: {0:0.3f}C'.format(temp))
