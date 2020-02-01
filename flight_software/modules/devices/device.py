from abc import ABC, abstractmethod

class Device(ABC):

    def __init__(self, name: str):
        self.name = name
    
    """
    Return true if the device is fully functional and calibrated, else return false
    """
    @abstractmethod
    def status(self) -> bool:
        pass

    """
    Reset the device. Return true if the device was successfully reset else false.
    """
    @abstractmethod
    def reset(self) -> bool:
        pass