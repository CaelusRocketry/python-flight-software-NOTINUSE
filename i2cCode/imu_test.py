# Reading data from a Sense HAT Raspberry Pi IMU
# Jason Chen @ Project Caelus
# 18 February, 2019

from sense_hat import SenseHat
import smbus
from smbus import SMBus

sense = SenseHat()
sense.show_message("Hello world")
"""
# i2c channel 1 is connected to the GPIO pins
channel = 1
# Address of the device (IMU in this case, defaults to 0x60)
address = 0x60
# Register address
reg_write_dac = 0x40

# Initialize i2c (SMBus)
bus = smbus.SMBus(channel)

# Create a sawtooth wave 16 times
for i in range(0x10000):

    # Create our 12-bit number representing relative voltage
    voltage = i & 0xfff

    # Shift everything left by 4 bits and separate bytes
    msg = (voltage & 0xff0) >> 4
    msg = [msg, (msg & 0xf) << 4]

    # Write out i2c command: address, reg_write_dac, msg[0], msg[1]
    bus.write_i2c_block_data(address, reg_write_dac, msg)
"""
