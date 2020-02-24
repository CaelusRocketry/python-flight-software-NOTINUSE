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
        gs_ip = config['GS_IP']
        gs_port = config['GS_PORT']
        delay = config['DELAY']
        self.telemetry.reset(gs_ip, gs_port, delay)

    def read(self, state_field_registry: Registry, flag: Flag) -> Registry:
        telemetry_packets = self.telemetry.read(-1)
        ingest_queue = state_field_registry.get("ingest_queue")
        for pack in telemetry_packets:
            ingest_queue.append(pack)

        err = state_field_registry.put("ingest_queue", ingest_queue)
        assert(err is AccessError.NONE)
        return state_field_registry
    
    def actuate(self, state_field_registry, flag: Flag) -> Flag:
        send_queue = flag.get("send_queue")
        for pack in send_queue:
            self.telemetry.write(pack)
        flag.put("send_queue", [])
        return flag
