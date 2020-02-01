import smbus
import struct

class Arduino(Device):

    def __init__(self, name: str, addr: hex, address):
        super(name)
        self.addr = addr
        self.address = address
        self.bus = smbus.SMBus(1)

    def status(self) -> bool:
        pass

    def reset(self) -> bool:
        pass

    """
    Read data from the Arduino and return it
    """
    def read(self) -> bytes:
        data = self.bus.read_i2c_block_data(self.address, 0, 4)
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
    