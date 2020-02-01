from abc import ABC, abstractmethod
from devices.device import Device
class Task:

    def __init__(self, name: str, dev: Device):
        self.name = name
        self.device = Device()
    
    """
    Read all data from the device and return the updated state field registry
    """
    @abstractmethod
    def read(self, state_field_registry: dict) -> dict:
        pass

    """
    Actuate if necessary, and return whether or not the actuation was successful
    """
    @abstractmethod
    def actuate(self, message: dict) -> bool:
        pass