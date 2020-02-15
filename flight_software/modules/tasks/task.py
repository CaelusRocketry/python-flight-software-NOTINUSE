from modules.drivers.driver import Driver
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from abc import ABC, abstractmethod

class Task:

    def __init__(self, name: str, driver: Driver):
        self.name = name
        self.driver = driver
    
    """
    Read all data from the device and return the updated state field registry
    """
    @abstractmethod
    def read(self, state_field_registry: Registry, flag: Flag) -> Registry:
        pass

    """
    Actuate if necessary, and return whether or not the actuation was successful
    """
    @abstractmethod
    def actuate(self, state_field_registry: Registry, flag: Flag) -> bool:
        pass