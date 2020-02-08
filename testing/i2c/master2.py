import struct
import smbus
import time

bus = smbus.SMBus(1)
address = 0x04

def get_data():
    return bus.read_i2c_block_data(address, 0, 4)

def get_float(data, index):
    # byte = data[4*index:(index+1)*4]
    byte_array = bytes(data)
    return struct.unpack('f', byte_array)[0]

while True:
    data = get_data()
    print(get_float(data, 0))
    time.sleep(.1)