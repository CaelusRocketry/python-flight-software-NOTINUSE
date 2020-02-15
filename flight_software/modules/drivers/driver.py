from abc import ABC, abstractmethod

class Driver(ABC):

    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
    
    """
    Return true if the device is fully functional and calibrated, else return false
    """
    @abstractmethod
    def read(self) -> bool:
        pass

    """
    Reset the device. Return true if the device was successfully reset else false.
    """
    @abstractmethod
    def write(self) -> bool:
        pass

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