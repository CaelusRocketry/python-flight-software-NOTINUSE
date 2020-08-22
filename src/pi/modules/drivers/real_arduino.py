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
        self.baud = config['baud']
        print(self.address, self.baud)
        self.name = name
        self.ser = serial.Serial(self.address, self.baud)
        self.reset()
        time.sleep(0.5)
    
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
        # Reset the arduino just like the serial monitor does: https://stackoverflow.com/questions/21073086/wait-on-arduino-auto-reset-using-pyserial
        self.ser.setDTR(False)
        time.sleep(1)
        self.ser.flush()
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.ser.setDTR(True)
        # Wait for arduino to reset
        time.sleep(3)


    """
    Read data from the Arduino and return it
    Ex. [10, 20, 0, 0, 15, 0, 0, 0, 14, 12, 74, 129]
    """
    def read(self, num_bytes: int) -> bytes:
        # TODO: ser.read() waits until the number of bytes requested is received, is this not good?
        print("Reading")
        data = bytearray()
        while len(data) < num_bytes:
            if self.ser.in_waiting:
                byt = self.ser.read()
                val = int.from_bytes(byt, 'big')
                # print(val)
                data.append(val)
        return bytes(data)

    """
    Write data to the Arduino and return True if the write was successful else False
    """
    def write(self, msg: bytes) -> bool:
        print("Writing:", msg)
        try:
            x = self.ser.write(msg) # x: the number of bytes that were written
            print(x)
            if x < len(msg):
                return False
            return True
        except:
            return False
        return False
    
