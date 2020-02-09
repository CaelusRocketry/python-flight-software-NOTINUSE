#!/usr/bin/python

import RPi.GPIO as GPIO
import smbus2
import struct
import time

slaveAddress = 0x04    

def readMessageFromArduino():
    global smsMessage
    data_received_from_Arduino = bytes(i2c.read_i2c_block_data(slaveAddress, 0, 4))
    print (struct.unpack('f', data_received_from_Arduino)[0])

if __name__ == '__main__':
    i2c = smbus2.SMBus(1)
    while 1:
        try:
            try:
                readMessageFromArduino() 
            except IOError:
                pass

        except KeyboardInterrupt:
            GPIO.cleanup()