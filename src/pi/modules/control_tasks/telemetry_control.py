import json
from heapq import heappop
from modules.mcl.flag import Flag
from modules.lib.errors import Error
from modules.mcl.registry import Registry
from modules.lib.packet import Packet, Log, LogPriority
from modules.lib.enums import SensorType, SensorLocation, ValveLocation, ActuationType, ValveType, Stage

class TelemetryControl(): 
    def __init__(self, registry: Registry, flag: Flag):
        self.registry = registry
        self.flag = flag
        self.funcs = {
            "heartbeat": self.heartbeat,
            "hard_abort": self.hard_abort,
            "soft_abort": self.soft_abort,
            "solenoid_actuate": self.solenoid_actuate,
            "sensor_request": self.sensor_request,
            "valve_request": self.valve_request,
            "progress": self.progress
        }
        self.arguments = {
            "heartbeat": (),
            "hard_abort": (),
            "soft_abort": (),
            "solenoid_actuate": (("valve_location", ValveLocation), ("actuation_type", ActuationType), ("priority", int)),
            "sensor_request": (("sensor_type", SensorType), ("sensor_location", SensorLocation)),
            "valve_request": (("valve_type", ValveType), ("valve_location", ValveLocation)),
            "progress": (),
        }

    def execute(self) -> Error:
        if self.registry.get(("telemetry", "status")) == False:
            self.flag.put(("telemetry", "reset"), True)
            return None

        self.flag.put(("telemetry", "reset"), False)
        err, telem_queue, _ = self.registry.get(("telemetry", "ingest_queue"))
        assert(err == Error.NONE)
        while telem_queue:
            packet = heappop(telem_queue)
            #TODO: Figure out if the command from a log is outdated
            for log in packet.logs:
                err = self.ingest(log)
                assert(err == Error.NONE)
            # Clear the ingest queue (because we just ingested everything)
            self.registry.put(("telemetry", "ingest_queue"), [])


    def ingest(self, log: Log):
        header = log.header
        if header in self.funcs:
            func = self.funcs[header]
            args = []
            assert(header in self.arguments)
            for arg_name, arg_type in self.arguments[header]:
                if arg_name not in log.message:
                    print("Invalid argument")
                    return Error.INVALID_ARGUMENT_ERROR
                elif not isinstance(log.message[arg_name], arg_type):
                    print("Invalid argument")
                    return Error.INVALID_ARGUMENT_ERROR
                args.append(log.message[arg_name])
            func(*args)
            return Error.NONE
        else:
            print("Invalid header")
            return Error.INVALID_HEADER_ERROR


    def enqueue(self, log: Log, level: LogPriority):
        err, queue = self.flag.get(("telemetry", "enqueue"))
        assert(err is Error.NONE)
        queue.append((log, level))
        err = self.flag.put(("telemetry", "enqueue"), queue)
        assert(err is Error.NONE)


    def heartbeat(self):
        self.enqueue(Log(header="heartbeat", message={"response": "OK"}), level=LogPriority.INFO)


    def hard_abort(self):
        self.registry.put(("abort", "hard_abort"), True)
        #TODO: For each valve, figure out what it's hard abort valve state is and add the flag for that at maximum priority
#        self.flag.put(("abort", "hard_abort"), valves)


    def soft_abort(self):
        self.registry.put(("abort", "soft_abort"), True)
        #TODO: For each valve, figure out what it's soft abort valve state is and add the flag for that at next to maximum priority
#        self.flag.put(("abort", "soft_abort"), valves)


    def solenoid_actuate(self, valve_location: ValveLocation, actuation_type: ActuationType, priority: int) -> Error:
        err, currnet_priority, timestamp = self.registry.get(("valve_actuation", "actuation_priority", ValveType.SOLENOID, location))
        if err != Error.NONE:
            #TODO: Send message back to gs saying it was an invalid message
            return Error.REQUEST_ERROR

        if priority <= currnet_priority:
            #TODO: Send message back to gs saying it was an invalid message
            return Error.PRIORITY_ERROR

        self.flag.put(("solenoid", "actuation_type", valve_location), actuation_type)
        self.flag.put(("solenoid", "actuation_priority", valve_location), actuation_type)


    def sensor_request(self, sensor_type: SensorType, sensor_location: SensorLocation) -> Error:
        err, value, timestamp = self.registry.get(("sensor", sensor_type, sensor_location))
        if err != Error.NONE:
            #TODO: Send message back to gs saying it was an invalid message
            return Error.REQUEST_ERROR
        err, status, _ = self.registry.get(("sensor_status", sensor_type, sensor_location))
        if err != Error.NONE:
            #TODO: Send message back to gs saying it was an invalid message
            return Error.REQUEST_ERROR

        log = Log(header="sensor_data", message={"type": sensor_type, "location": sensor_location, "value": value, "status": status, "timestamp": timestamp})
        self.enqueue(log, LogPriority.INFO)


    def valve_request(self, valve_type: ValveType, valve_location: ValveLocation) -> Error: 
        err, value, _ = self.registry.get(("valve", valve_type, valve_location))
        if err != Error.NONE:
            return Error.REQUEST_ERROR
        err, value, _ = self.registry.get(("valve_actuation", "actuation_type", valve_type, valve_location))
        if err != Error.NONE:
            return Error.REQUEST_ERROR
        err, value, timestamp = self.registry.get(("valve", "actuation_priority", valve_type, valve_location))
        if err != Error.NONE:
            return Error.REQUEST_ERROR

        log = Log(header="valve_data", message={"type": valve_type, "location": valve_location, "state": value, "actuation_type": valve_actuation, "actuation_priority": valve_actuation_priority, "actuation_timestamp": timestamp})
        self.enqueue(log, LogPriority.INFO)


    def progress(self, stage: Stage):
        self.flag.put(("progress", "stage"), stage)

