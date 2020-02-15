from modules.tasks.task import Task
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.drivers.telemetry_driver import Telemetry
from abc import ABC, abstractmethod

class TelemetryTask(Task):
    def __init__(self):
        self.telemetry = Telemetry()

    def read(self, state_field_registry: Registry, flag: Flag) -> Registry:
        telemetry_packets = telemetry.read()
        for i in telemetry_packets:
            state_field_registry.put("telemetry_queue", i, flag)
        return state_field_registry
    
    def actuate(self, state_field_registry, flag: Flag) -> bool:
        return True
