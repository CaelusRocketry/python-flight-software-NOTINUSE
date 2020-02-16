import struct
import smbus
import time

bus = smbus.SMBus(1)
address = 0x04

def get_data():
    return bus.read_i2c_block_data(address, 0, 12)

def get_float(data, index):
    data = data[index:index+4]
    byte_array = bytes(data)
    return struct.unpack('f', byte_array)[0]

while True:
    data = get_data()
    print(get_float(data, 0))
    print(get_float(data, 4))
    print(get_float(data, 8))
    print()
    
    time.sleep(1)