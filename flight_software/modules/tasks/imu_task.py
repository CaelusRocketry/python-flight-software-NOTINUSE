from task import Task
from abc import ABC, abstractmethod
from modules.devices.device import Device
from modules.supervisor.command import Command
from modules.supervisor.registry import Registry
from modules.supervisor.flags import Flag
from modules.drivers.imu_driver import IMU

class ImuTask(Task):
    def __init__(self):
        self.imu = IMU()
        self.flag = Flag()

    def read(self, state_field_registry: Registry) -> Registry:
        updatedDict = imu.read()
        for key in updatedDict:
            Registry.put(key, key.values(), flag)
        return Registry
    
    def actuate(self, command: Command) -> bool:
        return True
