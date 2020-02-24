from task import Task
from abc import ABC, abstractmethod
from modules.supervisor.command import Command
from modules.supervisor.registry import Registry
from modules.supervisor.flags import Flag
from modules.drivers.imu_driver import IMU

class ImuTask(Task):
    def __init__(self):
        self.imu = IMU()

    def read(self, state_field_registry: Registry, flag: Flag) -> Registry:
        updatedDict = imu.read()
        for key in updatedDict:
            state_field_registry.put(key, updatedDict[key])
        return state_field_registry
    
    def actuate(self, state_field_registry: Registry, flag: Flag) -> bool:
        if self.flag["imu_calibration"]:
            self.imu.calibrate()
    