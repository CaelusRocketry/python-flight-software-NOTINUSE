from task import Task
from abc import ABC, abstractmethod
from modules.devices.device import Device
from modules.supervisor.command import Command
from modules.supervisor.registry import Registry
from modules.supervisor.flags import Flag
from modules.drivers.imu_driver import IMU

class ImuTask(Task):
    def __init__(self, flag: Flag):
        self.imu = IMU()
        self.flag = flag

    def read(self, state_field_registry: Registry) -> Registry:
        updatedDict = imu.read()
        for key in updatedDict:
            state_field_registry.put(key, updatedDict[key])
        return state_field_registry
    
    def actuate(self) -> bool:
        if self.flag["imu_calibration"]:
            self.imu.calibrate()
    