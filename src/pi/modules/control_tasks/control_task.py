from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.lib.logging import Log, Packet, Level
from abc import ABC, abstractmethod

class ControlTask():
    def __init__(self):
        print("Config control task is active")

    def begin(self, config: dict):
        self.config = config

    def control(self, state_field_registry: Registry, flag: Flag) -> (Registry, Flag):
        queue = state_field_registry.get("ingest_queue")
        if len(queue) > 0:
            print([pack.to_string() for pack in queue])
            log = Log(header="HEARTBEAT", message="OK")
            pack = Packet(header="HEARTBEAT", logs=[log], level=Level.INFO)
            send_queue = flag.get("send_queue")
            send_queue.append(pack)
            flag.put("send_queue", send_queue)
        # Clear the ingest queue (because we just ingested everything)
        state_field_registry.put("ingest_queue", [])
        return state_field_registry, flag