from modules.tasks.task import Task
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.drivers.telemetry_driver import Telemetry
from modules.lib.errors import AccessError
from abc import ABC, abstractmethod

class TelemetryTask(Task):
    def __init__(self):
        self.telemetry = Telemetry()
        super().__init__("Telemetry", self.telemetry)

    def begin(self, config: dict):
        self.GS_IP = config['GS_IP']
        self.GS_PORT = config['GS_PORT']
        self.DELAY = config['DELAY']
        self.telemetry.reset(self.GS_IP, self.GS_PORT, self.DELAY)

    def read(self, state_field_registry: Registry, flag: Flag) -> Registry:
        telemetry_status = self.telemetry.status()
        state_field_registry.put(("telemetry", "status"), telemetry_status)
        if telemetry_status == False:
            return state_field_registry

        telemetry_packets = self.telemetry.read(-1)
        ingest_queue = state_field_registry.get(("telemetry", "ingest_queue"))
        for pack in telemetry_packets:
            ingest_queue.append(pack)

        err = state_field_registry.put(("telemetry", "ingest_queue"), ingest_queue)
        assert(err is AccessError.NONE)
        return state_field_registry
    
    def actuate(self, state_field_registry, flag: Flag) -> Flag:
        if flag.get(("telemetry", "reset")) == True:
            self.telemetry.reset(self.GS_IP, self.GS_PORT, self.DELAY)

        send_queue = flag.get(("telemetry", "send_queue"))
        for pack in send_queue:
            self.telemetry.write(pack)
        flag.put(("telemetry", "send_queue"), [])
        return flag
