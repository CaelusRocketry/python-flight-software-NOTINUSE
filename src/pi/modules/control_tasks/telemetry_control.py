import json, enum
from heapq import heappop
from modules.mcl.flag import Flag
from modules.lib.errors import Error
from modules.mcl.registry import Registry
from modules.lib.packet import Packet, Log, LogPriority
from modules.lib.enums import SensorType, SensorLocation, ValveLocation, ActuationType, ValveType, Stage
import time

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
    

    def begin(self, config: dict):
        self.config = config
        self.sensors = config["sensors"]["list"]
        self.valves = config["valves"]["list"]


    def execute(self) -> Error:
        #TODO: Check if resetting telemetry works
        _, status, timestamp = self.registry.get(("telemetry", "status"))
        if not status:
            self.flag.put(("telemetry", "reset"), True)
            return None

        self.flag.put(("telemetry", "reset"), False)
        _, telem_queue, _ = self.registry.get(("telemetry", "ingest_queue"))
        while telem_queue:
            packet = heappop(telem_queue)
            #TODO: Figure out if the command from a log is outdated
            for log in packet.logs:
                err = self.ingest(log)
                assert(err == Error.NONE)
            # Clear the ingest queue (because we just ingested everything)
            self.registry.put(("telemetry", "ingest_queue"), [])


    def ingest(self, log: Log):
        #TODO: Send message back to GS saying that an invalid message was sent
        header = log.header
        if header in self.funcs:
            func = self.funcs[header]
            args = []
            assert(header in self.arguments)
            for arg_name, arg_type in self.arguments[header]:
                if arg_name not in log.message:
                    print("Invalid argument", arg_name)
                    log = Log(header="response", message={"action": ("Ingest: invalid argument: " + arg_name), "priority": 1, "timestamp": time.time()})
                    self.enqueue(log, LogPriority.CRIT)
                    return Error.INVALID_ARGUMENT_ERROR
                if issubclass(arg_type, enum.Enum):
                    if log.message[arg_name] not in [x.value for x in arg_type]:
                        print("Invalid argument", arg_name, arg_type)
                        log = Log(header="response", message={"action": ("Ingest: in: " + arg_name + ", invalid argument: " + log.message[arg_name] + " with type: " + arg_type), "priority": 1, "timestamp": time.time()})
                        self.enqueue(log, LogPriority.CRIT)
                        return Error.INVALID_ARGUMENT_ERROR
                elif not isinstance(log.message[arg_name], arg_type):
                    print("Invalid argument", arg_name, arg_type)
                    log = Log(header="response", message={"action": ("Ingest: in: " + arg_name + ", argument: " + log.message[arg_name] + ", invalid type: " + arg_type), "priority": 1, "timestamp": time.time()})
                    self.enqueue(log, LogPriority.CRIT)
                    return Error.INVALID_ARGUMENT_ERROR
                args.append(arg_type(log.message[arg_name]))
            func(*args)
            return Error.NONE
        else:
            print("Invalid header")
            return Error.INVALID_HEADER_ERROR


    def enqueue(self, log: Log, level: LogPriority):
        _, queue = self.flag.get(("telemetry", "enqueue"))
        queue.append((log, level))
        self.flag.put(("telemetry", "enqueue"), queue)


    def heartbeat(self):
        self.enqueue(Log(header="heartbeat", message={"response": "OK"}), level=LogPriority.INFO)


    def hard_abort(self):
        self.flag.put(("general", "hard_abort"), True)


    def soft_abort(self):
        self.flag.put(("general", "soft_abort"), True)


    def solenoid_actuate(self, valve_location: ValveLocation, actuation_type: ActuationType, priority: int) -> Error:
        err, current_priority, timestamp = self.registry.get(("valve_actuation", "actuation_priority", ValveType.SOLENOID, valve_location), allow_error=True)
        if err != Error.NONE:
            # Send message back to gs saying it was an invalid message
            log = Log(header="response", message={"action": ("Unable to actuate solenoid at " + valve_location + " with actuation type " + actuation_type), "priority": priority, "timestamp": timestamp})
            self.enqueue(log, LogPriority.CRIT)
            return Error.REQUEST_ERROR

        if priority <= current_priority:
            # Send message back to gs saying that the request was made w/ too little priority
            log = Log(header="response", message={"action": ("Too little priority: unable to actuate solenoid at " + valve_location + " with actuation type " + actuation_type + " at priority " + str(priority)), "priority": priority, "timestamp": timestamp})
            self.enqueue(log, LogPriority.CRIT)
            return Error.PRIORITY_ERROR

        print("Actuating solenoid at {} with actuation type {}".format(valve_location, actuation_type))

        self.flag.put(("solenoid", "actuation_type", valve_location), actuation_type)
        self.flag.put(("solenoid", "actuation_priority", valve_location), priority)


    def sensor_request(self, sensor_type: SensorType, sensor_location: SensorLocation) -> Error:
        err, value, timestamp = self.registry.get(("sensor", sensor_type, sensor_location), allow_error=True)
        if err != Error.NONE:
            # Send message back to gs saying it was an invalid message            
            log = Log(header="response", message={"action": ("Unable to request " + sensor_type + " data from " + sensor_location), "priority": 1, "timestamp": timestamp})
            self.enqueue(log, LogPriority.CRIT)
            return Error.REQUEST_ERROR
        _, status, _ = self.registry.get(("sensor_status", sensor_type, sensor_location))
        log = Log(header="sensor_data", message={"type": sensor_type, "location": sensor_location, "value": value, "status": status, "timestamp": timestamp})
        self.enqueue(log, LogPriority.INFO)


    def valve_request(self, valve_type: ValveType, valve_location: ValveLocation) -> Error: 
        err, value, timestamp = self.registry.get(("valve", valve_type, valve_location), allow_error=True)
        if err != Error.NONE:
            # Send message back to gs saying it was an invalid message            
            log = Log(header="response", message={"action": ("Unable to request " + valve_type + " data from " + valve_location), "priority": 1, "timestamp": timestamp})
            self.enqueue(log, LogPriority.CRIT)
            return Error.REQUEST_ERROR

        _, actuation_type, timestamp = self.registry.get(("valve_actuation", "actuation_type", valve_type, valve_location))
        _, actuation_priority, _ = self.registry.get(("valve", "actuation_priority", valve_type, valve_location))
        log = Log(header="valve_data", message={"type": valve_type, "location": valve_location, "state": value, "actuation_type": actuation_type, "actuation_priority": actuation_priority, "actuation_timestamp": timestamp})
        self.enqueue(log, LogPriority.INFO)


    def progress(self, stage: Stage):
        self.flag.put(("progress", "stage"), stage)

