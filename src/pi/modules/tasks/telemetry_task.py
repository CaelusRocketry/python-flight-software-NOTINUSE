from modules.tasks.task import Task
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.drivers.telemetry_driver import Telemetry
from modules.lib.errors import Error
from abc import ABC, abstractmethod

class TelemetryTask(Task):
    def __init__(self, registry: Registry, flag: Flag):
        self.registry = registry
        self.flag = flag

    def begin(self, config: dict):
        self.GS_IP = config['GS_IP']
        self.GS_PORT = config['GS_PORT']
        self.DELAY = config['DELAY']
        self.telemetry = Telemetry(config)
        self.telemetry.connect()


    # Read telemetry packets and update the respective fields in the state field registry
    def read(self):
        telemetry_status = self.telemetry.status()
        err = self.registry.put(("telemetry", "status"), telemetry_status)
        assert(err is Error.NONE)
        if not telemetry_status:
            return

        telemetry_packets = self.telemetry.read(-1)
        err, ingest_queue, _ = self.registry.get(("telemetry", "ingest_queue"))
        assert(err is Error.NONE)
        for pack in telemetry_packets:
            ingest_queue.append(pack)

        err = self.registry.put(("telemetry", "ingest_queue"), ingest_queue)
        assert(err is Error.NONE)


    def actuate(self) -> Flag:
        err, telemetry_reset = self.flag.get(("telemetry", "reset"))
        assert(err is Error.NONE)
        if telemetry_reset:
            self.telemetry.reset()
            return

        err, send_queue = self.flag.get(("telemetry", "send_queue"))
        assert(err is Error.NONE)
        for pack in send_queue:
            self.telemetry.write(pack)
        err = self.flag.put(("telemetry", "send_queue"), [])
        assert(err is Error.NONE)
