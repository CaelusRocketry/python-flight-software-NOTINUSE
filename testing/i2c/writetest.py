import smbus
import time
import os

bus = smbus.SMBus(1)

i2c_address = 0x04
i2c_cmd = 0x01

exit = False
while not exit:
    r = input('Enter something, "q" to quit"')
    print(r)
    
    bytesToSend = [ord(b) for b in r]
    bus.write_i2c_block_data(i2c_address, i2c_cmd, bytesToSend)
    
    if r=='q':
        exit=True