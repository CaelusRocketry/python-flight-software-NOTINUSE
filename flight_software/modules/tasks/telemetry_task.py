from task import Task
from task import Task
from abc import ABC, abstractmethod
from modules.devices.device import Device
from modules.supervisor.command import Command
from modules.supervisor.registry import Registry
from modules.supervisor.flags import Flag
from modules.drivers.telemetry_driver import Telemetry

class TelemetryTask(Task):
    def __init__(self):
        self.telemetry = Telemetry()
        self.flag = Flag()

    def read(self, state_field_registry: Registry) -> Registry:
        telemetry_packets = telemetry.read()
        for i in telemetry_packets:
            Registry.put("telemetry_queue", i, flag)
        return Registry
    
    def actuate(self, command: Command) -> bool:
        return True