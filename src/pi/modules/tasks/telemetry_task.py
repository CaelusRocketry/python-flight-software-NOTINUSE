from modules.mcl.flag import Flag
from abc import ABC, abstractmethod
from modules.tasks.task import Task
from modules.lib.errors import Error
from modules.mcl.registry import Registry
from modules.drivers.telemetry_driver import Telemetry
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
        

    def enqueue(self, log: Log, priority: LogPriority):
        # TODO: This is implemented wrong. It should enqueue by finding packets that have similar priorities, not changing the priorities of current packets.
        _, send_queue = self.flag.get(("telemetry", "send_queue"))
        if send_queue:
            pack = send_queue[0]
            pack.priority = max(pack.priority, priority)
            pack.add(log)
        else:
            pack = Packet(logs=[log], priority=priority)
            send_queue.append(pack)
            self.flag.put(("telemetry", "send_queue"), send_queue)


    def actuate(self) -> Flag:
        _, telemetry_reset = self.flag.get(("telemetry", "reset"))
        if telemetry_reset:
            self.telemetry.reset()
            return
        
        _, enqueue_queue = self.flag.get(("telemetry", "enqueue"))
        for log, priority in enqueue_queue:
            self.enqueue(log, priority)
        self.flag.put(("telemetry", "enqueue"), [])
        
        _, send_queue = self.flag.get(("telemetry", "send_queue"))

        for pack in send_queue:
            err = self.telemetry.write(pack)
            if err != Error.NONE:
                print("Telemetry connection lost while sending")
                return
        self.flag.put(("telemetry", "send_queue"), [])
