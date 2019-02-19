# Reading data from a Sense HAT Raspberry Pi IMU
# Jason Chen @ Project Caelus
# 18 February, 2019

from sense_hat import SenseHat
import time
from datetime import datetime
import threading
# import smbus
# from smbus import SMBus

def startup():
    global sense
    sense = SenseHat()
    sense.show_message("Hello world!")
    time.sleep(5)

def mainloop():
    while True:
        epoch = datetime.utcnow()
        print('{:-^20}'.format(" Report for " + epoch.strftime(" % Y-%m-%d % H: % M: % S") + " UTC. "))
        print("Pressure (mBar):", '\t', sense.get_pressure())
        print("Temperature (C):", '\t', sense.get_temperature())
        print("Humidity (%):", '\t', sense.get_humidity())
        time.sleep(5)

def orientation():
    while True:
        o = sense.get_orientation()
        pitch = o["pitch"]
        roll = o["roll"]
        yaw = o["yaw"]
        print("Pitch: {0:6.3f}".format(pitch), '\t', "Roll: {0:6.3f}".format(roll), '\t', "Yaw: {0:6.3f}".format(yaw))

if __name__ == "__main__":
    startup()
    t1 = threading.Thread(target=mainloop, args=(), daemon=True)
    t1.start()
    t2 = threading.Thread(target=orientation, args=(), daemon=True)
    t2.start()
    t1.join()
    t2.join()

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
