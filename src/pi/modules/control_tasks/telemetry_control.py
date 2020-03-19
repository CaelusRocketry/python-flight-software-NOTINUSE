from modules.mcl.flag import Flag
from modules.mcl.registry import Registry
from modules.lib.enums import SensorType, SensorLocation, ValveLocation, ActuationType, ValveType
from modules.lib.errors import AccessError, Error
from modules.lib.packet import Packet, Log, LogPriority
import json

class TelemetryControl(): 
    def __init__(self, registry: Registry, flags: Flag):
        self.registry = registry
        self.flags = flags
        self.funcs = {
            "heartbeat": heartbeat,
            "hard_abort": hard_abort,
            "soft_abort": soft_abort,
            "solenoid_actuate": solenoid_actuate,
            "sensor_request": sensor_request,
            "valve_request": valve_request,
            "progress": progress
        }
        self.arguments = {
            "heartbeat": (),
            "hard_abort": (),
            "soft_abort": (),
            "solenoid_actuate": (("valve_location", ValveLocation), ("actuation_type", ActuationType), ("priority", priority)),
            "sensor_request": (("sensor_type", SensorType), ("sensor_location", SensorLocation)),
            "valve_request": (("valve_type", ValveType), ("valve_location", ValveLocation)),
            "progress": (),
        }

    def execute(self) -> Error:
        if registry.get(("telemetry", "status")) == False:
            self.flags.put(("telemetry", "reset"), True)
            return None

        self.flags.put(("telemetry", "reset"), False)
        err, telem_queue, _ = registry.get(("telemetry", "ingest_queue"))
        assert(err == AccessError.NONE)
        if telem_queue:
            for packet in telem_queue:
                #TODO: Figure out if the command from a log is outdated
                for log in packet:
                    err = self.ingest(log)
                    assert(err == Error.NONE)
            # Clear the ingest queue (because we just ingested everything)
            self.registry.put(("telemetry", "ingest_queue"), [])


    def ingest(self, log: Log):
        header = log.header
        if header in funcs:
            func = funcs[header]
            args = []
            assert(header in self.arguments)
            for arg_name, arg_type in self.arguments[header]:
                if arg_name not in log.message:
                    return Error.INVALID_ARGUMENT_ERROR
                elif not isinstance(log.message[arg_name], arg_type):
                    return Error.INVALID_ARGUMENT_ERROR
                args.append(log.message[arg_name])
            func(*args)
            return Error.NONE
        else:
            self.enqueue(Log(header="InvalidHeader", message={"received_header": log.header, "received_message": log.message}), LogPriority.WARN)
            return Error.INVALID_HEADER_ERROR


    def enqueue(self, log: Log, level: LogPriority):
        added = False
        send_queue = self.flags.get(("telemetry", "send_queue"))
        for pack in send_queue:
            if pack.level == level:
                pack.add(log)
                added = True
                break
        if not added:
            pack = Packet(logs=[log], level=LogPriority.INFO)
            send_queue.append(pack)
        self.flags.put(("telemetry", "send_queue"), send_queue)


    def heartbeat(self):
        self.enqueue(Log(header="HEARTBEAT", message={"response": "OK"}))


    def hard_abort(self):
        self.registry.put(("abort", "hard_abort"), True)
        #TODO: For each valve, figure out what it's hard abort valve state is and add the flag for that at maximum priority
#        self.flags.put(("abort", "hard_abort"), valves)


    def soft_abort(self):
        self.registry.put(("abort", "soft_abort"), True)
        #TODO: For each valve, figure out what it's soft abort valve state is and add the flag for that at next to maximum priority
#        self.flags.put(("abort", "soft_abort"), valves)


    def solenoid_actuate(self, valve_location: ValveLocation, actuation_type: ActuationType, priority: int) -> Error:
        err, currnet_priority, timestamp = self.registry.get(("valve_actuation", "actuation_priority", ValveType.SOLENOID, location))
        if err != AccessError.NONE:
            #TODO: Send message back to gs saying it was an invalid message
            return Error.REQUEST_ERROR

        if priority <= currnet_priority:
            #TODO: Send message back to gs saying it was an invalid message
            return Error.PRIORITY_ERROR

        self.flags.put(("solenoid", "actuation_type", valve_location), actuation_type)
        self.flags.put(("solenoid", "actuation_priority", valve_location), actuation_type)


    def sensor_request(self, sensor_type: SensorType, sensor_location: SensorLocation) -> Error:
        err, value, timestamp = self.registry.get(("sensor", sensor_type, sensor_location))
        if err != AccessError.NONE:
            #TODO: Send message back to gs saying it was an invalid message
            return Error.SENSOR_REQUEST_ERROR
        err, status, _ = self.registry.get(("sensor_status", sensor_type, sensor_location))
        if err != AccessError.NONE:
            #TODO: Send message back to gs saying it was an invalid message
            return Error.SENSOR_REQUEST_ERROR

        log = Log(header="sensor_data", message={"type": sensor_type, "location": sensor_location, "value": value, "status": status, "timestamp": timestamp})
        self.enqueue(log, LogPriority.INFO)


    def valve_request(self, valve_type: ValveType, valve_location: ValveLocation) -> Error: 
        err, value, _ = self.registry.get(("valve", valve_type, valve_location))
        if err != AccessError.NONE:
            return Error.REQUEST_ERROR
        err, value, _ = self.registry.get(("valve_actuation", "actuation_type", valve_type, valve_location))
        if err != AccessError.NONE:
            return Error.REQUEST_ERROR
        err, value, timestamp = self.registry.get(("valve", "actuation_priority", valve_type, valve_location))
        if err != AccessError.NONE:
            return Error.REQUEST_ERROR

        log = Log(header="valve_data", message={"type": valve_type, "location": valve_location, "state": value, "actuation_type": valve_actuation, "actuation_priority": valve_actuation_priority, "actuation_timestamp": timestamp})
        self.enqueue(log, LogPriority.INFO)


    def progress(self, stage: Stage):
        self.flags.put(("progress", "stage"), stage)

