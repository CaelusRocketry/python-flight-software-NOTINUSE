

class Arduino(Device):

    def __init__(self, name: str, addr: hex):
        super(name)
        self.addr = addr

    def status(self) -> bool:
        pass

    def reset(self) -> bool:
        pass

    """
    Read data from the Arduino and return it
    """
    def read(self) -> bytes:
        pass

    """
    Write data to the Arduino and return True if the write was successful else False
    """
    def write(self, msg: bytes) -> bool:
        pass
    