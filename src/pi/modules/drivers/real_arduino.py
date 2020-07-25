from .driver import Driver
import smbus2 as smbus
import struct

class Arduino(Driver):

    def __init__(self, name: "str", config: dict):
        super().__init__(name)
        self.config = config
        self.address = config['address']
        print(self.address)
        self.bus = smbus.SMBus(1)
    
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
        data = self.bus.read_i2c_block_data(self.address, 0, num_bytes)
        print(data)
        byte_array = bytes(data)
        # return struct.unpack('f', byte_array)[0]
        return byte_array

    """
    Write data to the Arduino and return True if the write was successful else False
    """
    def write(self, msg: bytes) -> bool:
        # converts string to bytes : msg = [ord(b) for b in src]
        try:
            self.bus.write_i2c_block_data(self.address, 0x01, msg)
            return True
        except:
            return False
        pass
    
