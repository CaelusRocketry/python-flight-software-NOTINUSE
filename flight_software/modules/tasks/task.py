from abc import ABC, abstractmethod
from modules.devices.device import Device
from modules.supervisor.command import Command
from modules.supervisor.registry import Registry
class Task:

    def __init__(self, name: str, dev: Device):
        self.name = name
        self.device = Device()
    
    """
    Read all data from the device and return the updated state field registry
    """
    @abstractmethod
    def read(self, state_field_registry: Registry) -> Registry:
        pass

    """
    Actuate if necessary, and return whether or not the actuation was successful
    """
    @abstractmethod
    def actuate(self, command: Command) -> bool:
        pass