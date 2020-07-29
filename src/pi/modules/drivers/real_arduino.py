from .driver import Driver
# import smbus2 as smbus
import serial
import time
import struct

class Arduino(Driver):

    def __init__(self, name: "str", config: dict):
        super().__init__(name)
        self.config = config
        self.address = config['address']
        self.name = '/dev/ttyACM0' # TODO: find out what the name is on our pi https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/
        self.baud = 9600
        print(self.address)
        self.ser = serial.Serial(name, baud)
        ser.flush()
    
    """
    Return whether or not the i2c connection is alive
    """
    def status(self) -> bool:
        # ping = "hey u alive"
        # ping_bytes = [ord(b) for b in ping]
        # self.write(ping_bytes)

        # time.sleep(.3)

        # response = self.read()
        # return struct.unpack('f', response)[0] == "yeah i'm good"
        pass

    """
    Powercycle the arduino
    """
    def reset(self) -> bool:
        pass

    """
    Read data from the Arduino and return it
    Ex. [10, 20, 0, 0, 15, 0, 0, 0, 14, 12, 74, 129]
    """
    def read(self, num_bytes: int) -> bytes:
        # TODO: ser.read() waits until the number of bytes requested is received, is this not good?
        data = ser.read(num_bytes)
        
        byte_array = bytes(data)
        # return struct.unpack('f', byte_array)[0]
        return byte_array

    """
    Write data to the Arduino and return True if the write was successful else False
    """
    def write(self, msg: bytes) -> bool:
        # converts string to bytes : msg = [ord(b) for b in src]
        try:
            x = ser.write(msg) # x: the number of bytes that were written
            if x < len(msg):
                return False
            return True
        except:
            return False
        return False
    
