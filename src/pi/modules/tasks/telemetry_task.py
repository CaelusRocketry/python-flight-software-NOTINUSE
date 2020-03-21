from modules.tasks.task import Task
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.drivers.telemetry_driver import Telemetry
from abc import ABC, abstractmethod
from modules.lib.packet import Log, Packet, LogPriority

class TelemetryTask(Task):
    def __init__(self, registry: Registry, flag: Flag):
        self.registry = registry
        self.flag = flag


    def begin(self, config: dict):
        self.config = config["telemetry"]
        print(self.config)
        self.GS_IP = self.config['GS_IP']
        self.GS_PORT = self.config['GS_PORT']
        self.DELAY = self.config['DELAY']
        self.telemetry = Telemetry(self.GS_IP, self.GS_PORT, self.DELAY)
        self.telemetry.connect()


    # Read telemetry packets and update the respective fields in the state field registry
    def read(self):
        telemetry_status = self.telemetry.status()
        self.registry.put(("telemetry", "status"), telemetry_status)
        if not telemetry_status:
            return

        telemetry_packets = self.telemetry.read(-1)
        _, ingest_queue, _ = self.registry.get(("telemetry", "ingest_queue"))
        for pack in telemetry_packets:
            ingest_queue.append(pack)

        self.registry.put(("telemetry", "ingest_queue"), ingest_queue)
        

    def enqueue(self, log: Log, level: LogPriority):
        added = False
        _, send_queue = self.flag.get(("telemetry", "send_queue"))
        for pack in send_queue:
            if pack.level == level:
                pack.add(log)
                added = True
                break
        if not added:
            pack = Packet(logs=[log], level=LogPriority.INFO)
            send_queue.append(pack)
        self.flag.put(("telemetry", "send_queue"), send_queue)


    def actuate(self) -> Flag:
        _, telemetry_reset = self.flag.get(("telemetry", "reset"))
        if telemetry_reset:
            self.telemetry.reset()
            return
        
        _, enqueue_queue = self.flag.get(("telemetry", "enqueue"))
        for log, level in enqueue_queue:
            self.enqueue(log, level)
        self.flag.put(("telemetry", "enqueue"), [])
        
        _, send_queue = self.flag.get(("telemetry", "send_queue"))
        for pack in send_queue:
            self.telemetry.write(pack)
        self.flag.put(("telemetry", "send_queue"), [])
