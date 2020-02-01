

class Arduino(Device):

    def __init__(self, name: str, addr: hex):
        super(name)
        self.addr = addr
    
    def status(self) -> bool:
        pass

    def reset(self) -> bool:
        pass

    """
    Read data from the Arduino
    """
    def read(self) -> bytes:
        pass

    """
    Write data to the Arduino
    """
    def write(self, msg: bytes) -> bytes:
        pass
    