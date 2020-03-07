from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.lib.packet import Log, Packet, Level
from abc import ABC, abstractmethod
import time

class ControlTask():
    def __init__(self):
        print("Config control task is active")
        self.controls = []

    def begin(self, config: dict):
        self.config = config
        if self.config["telemetry_control"]:
            self.controls.append(self.telemetry_control)
        if self.config["sensor_control"]:
            self.controls.append(self.sensor_control)
        if self.config["valve_control"]:
            self.controls.append(self.valve_control)

    def control(self, state_field_registry: Registry, flag: Flag) -> (Registry, Flag):
        for ctrl in self.controls:
            state_field_registry, flag = ctrl(state_field_registry, flag)
        return state_field_registry, flag

    def telemetry_control(self, state_field_registry: Registry, flag: Flag) -> (Registry, Flag):
        if state_field_registry.get(("telemetry", "status")) == False:
            flag.put(("telemetry", "reset"), True)
            return state_field_registry, flag

        flag.put(("telemetry", "reset"), False)
        queue = state_field_registry.get(("telemetry", "ingest_queue"))
        if len(queue) > 0:
            print([pack.to_string() for pack in queue])
            log = Log(header="HEARTBEAT", message="OK")
            pack = Packet(header="HEARTBEAT", logs=[log], level=Level.INFO)
            send_queue = flag.get(("telemetry", "send_queue"))
            send_queue.append(pack)
            flag.put(("telemetry", "send_queue"), send_queue)
        # Clear the ingest queue (because we just ingested everything)
        state_field_registry.put(("telemetry", "ingest_queue"), [])
        return state_field_registry, flag

    def sensor_control(self, state_field_registry: Registry, flag: Flag) -> (Registry, Flag):
        print(state_field_registry.to_string())
        time.sleep(1)
        return state_field_registry, flag
    
    def valve_control(self, state_field_registry: Registry, flag: Flag) -> (Registry, Flag):
        return state_field_registry, flag