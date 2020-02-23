from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from abc import ABC, abstractmethod

class ControlTask():
    def __init__(self):
        print("Config control task is active")

    def begin(self, config: dict):
        self.config = config

    def control(self, state_field_registry: Registry, flag: Flag) -> (Registry, Flag):
        queue = state_field_registry.get("telemetry_queue")
        if len(queue) > 0:
            print([pack.to_string() for pack in queue])
        state_field_registry.put("telemetry_queue", [])
        return state_field_registry, flag