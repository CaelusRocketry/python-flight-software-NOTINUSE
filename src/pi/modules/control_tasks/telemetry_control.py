import json, enum, time
from heapq import heappop
from modules.mcl.flag import Flag
from modules.lib.errors import Error
from modules.lib.helpers import enqueue
from modules.mcl.registry import Registry
from modules.lib.packet import Packet, Log, LogPriority
from modules.lib.enums import SensorType, SensorLocation, ValveLocation, ActuationType, ValveType, ValvePriority, Stage

class TelemetryControl(): 
    def __init__(self, registry: Registry, flag: Flag):
        self.registry = registry
        self.flag = flag
        # TODO: Add an "undo_soft_abort" function
        self.funcs = {
            "heartbeat": self.heartbeat,
            "soft_abort": self.soft_abort,
            "solenoid_actuate": self.solenoid_actuate,
            "sensor_request": self.sensor_request,
            "valve_request": self.valve_request,
            "progress": self.progress,
            "test": self.test,
        }
        self.arguments = {
            "heartbeat": (),
            "soft_abort": (),
            "solenoid_actuate": (("valve_location", ValveLocation), ("actuation_type", ActuationType), ("priority", ValvePriority)),
            "sensor_request": (("sensor_type", SensorType), ("sensor_location", SensorLocation)),
            "valve_request": (("valve_type", ValveType), ("valve_location", ValveLocation)),
            "progress": (),
            "test": (("response", str),)
        }
    

    def begin(self, config: dict):
        self.config = config


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
                print(log)
                err = self.ingest(log)
            # Clear the ingest queue (because we just ingested everything)
            self.registry.put(("telemetry", "ingest_queue"), [])


    def ingest(self, log: Log):
        header = log.header
        if header in self.funcs:
            func = self.funcs[header]
            args = []
            assert(header in self.arguments)
            # Loop through each of the arguments
            for arg_name, arg_type in self.arguments[header]:
                # If you can't find the argument in the 'message' section, throw an exception.
                if arg_name not in log.message:
                    print("Invalid argument", arg_name)
                    log = Log(header="response", message={"header": "Missing argument", "Argument": arg_name})
                    enqueue(self.flag, log, LogPriority.CRIT)
                    return Error.INVALID_ARGUMENT_ERROR
                # If its an enum, then make it an enum
                if issubclass(arg_type, enum.Enum):
                    if log.message[arg_name] not in [x.value for x in arg_type]:
                        print("Invalid argument", arg_name, arg_type)
                        log = Log(header="response", message={"header": "Invalid argument type", "Argument": arg_name, "Received argument type": str(type(log.message[arg_name])), "Expected argument type (enum)": str(arg_type)})
                        enqueue(self.flag, log, LogPriority.CRIT)
                        return Error.INVALID_ARGUMENT_ERROR
                # Otherwise, take the raw value
                elif not isinstance(log.message[arg_name], arg_type):
                    print("Invalid argument", arg_name, arg_type)
                    log = Log(header="response", message={"header": "Invalid argument type", "Argument": arg_name, "Received argument type": str(type(log.message[arg_name])), "Expected argument type": str(arg_type)})
                    enqueue(self.flag, log, LogPriority.CRIT)
                    return Error.INVALID_ARGUMENT_ERROR
                args.append(arg_type(log.message[arg_name]))
            # Run the command w/ the given arguments
            print("Running command (via telemetry):", header, *args)
            func(*args)
            return Error.NONE
        else:
            print("Invalid header")
            log = Log(header="response", message={"header": "Invalid telemetry header", "Telemetry header": header})
            enqueue(self.flag, log, LogPriority.CRIT)
            return Error.INVALID_HEADER_ERROR


    def heartbeat(self):
        enqueue(self.flag, Log(header="heartbeat", message={"response": "OK", "mode": "Soft abort" if self.registry.get(("general", "soft_abort"))[1] else "Normal"}), LogPriority.INFO)
        print("mode", self.registry.get(("general", "soft_abort"))[1])


    def soft_abort(self):
        self.registry.put(("general", "soft_abort"), True)
        log = Log(header="response", message={"header": "Soft abort", "Status": "Success", "Description": "Rocket is undergoing soft abort"})
        enqueue(self.flag, log, LogPriority.CRIT)
        enqueue(self.flag, Log(header="mode", message={"mode": "Soft abort"}), LogPriority.CRIT)


    def solenoid_actuate(self, valve_location: ValveLocation, actuation_type: ActuationType, priority: int) -> Error:
        err, current_priority, timestamp = self.registry.get(("valve_actuation", "actuation_priority", ValveType.SOLENOID, valve_location), allow_error=True)
        if err != Error.NONE:
            # Send message back to gs saying it was an invalid message
            log = Log(header="response", message={"header": "Valve actuation", "Status": "Failure", "Description": "Unable to find actuatable solenoid", "Provided valve location": valve_location})
            enqueue(self.flag, log, LogPriority.CRIT)
            return Error.REQUEST_ERROR

        if priority > current_priority:
            # Send message back to gs saying that the request was made w/ too little priority
            log = Log(header="response", message={"header": "Valve actuation", "Status": "Failure", "Description": "Too little priority to actuate solenoid", "Valve location": valve_location, "Actuation type": actuation_type, "Priority": priority})
            enqueue(self.flag, log, LogPriority.CRIT)
            return Error.PRIORITY_ERROR

        print("Actuating solenoid at {} with actuation type {}".format(valve_location, actuation_type))

        self.flag.put(("solenoid", "actuation_type", valve_location), actuation_type)
        self.flag.put(("solenoid", "actuation_priority", valve_location), priority)

        log = Log(header="response", message={"header": "Valve actuation", "Status": "Success", "Description": "Successfully actuated solenoid", "Valve location": valve_location, "Actuation type": actuation_type, "Priority": priority})
        enqueue(self.flag, log, LogPriority.CRIT)


    def sensor_request(self, sensor_type: SensorType, sensor_location: SensorLocation) -> Error:
        err, value, timestamp = self.registry.get(("sensor_measured", sensor_type, sensor_location), allow_error=True)
        if err != Error.NONE:
            # Send message back to gs saying it was an invalid message            
            log = Log(header="response", message={"header": "Sensor data", "Status": "Failure", "Description": "Unable to find sensor", "Type": sensor_type, "Location": sensor_location})
            enqueue(self.flag, log, LogPriority.CRIT)
            return Error.REQUEST_ERROR

        _, kalman_value, _ = self.registry.get(("sensor_normalized", sensor_type, sensor_location), allow_error=True)
        _, status, _ = self.registry.get(("sensor_status", sensor_type, sensor_location))
        log = Log(header="response", message={"header": "Sensor data", "Status": "Success", "Sensor type": sensor_type, "Sensor location": sensor_location, "Measured value": value, "Normalized value": kalman_value, "Sensor status": status, "Last updated": timestamp})
        enqueue(self.flag, log, LogPriority.INFO)


    def valve_request(self, valve_type: ValveType, valve_location: ValveLocation) -> Error: 
        err, value, timestamp = self.registry.get(("valve", valve_type, valve_location), allow_error=True)
        if err != Error.NONE:
            # Send message back to gs saying it was an invalid message            
            log = Log(header="response", message={"header": "Valve data request", "Status": "Failure", "Description": "Unable to find valve", "Valve type": valve_type, "Valve location": valve_location})
            enqueue(self.flag, log, LogPriority.CRIT)
            return Error.REQUEST_ERROR

        _, actuation_type, timestamp = self.registry.get(("valve_actuation", "actuation_type", valve_type, valve_location))
        _, actuation_priority, _ = self.registry.get(("valve_actuation", "actuation_priority", valve_type, valve_location))
        log = Log(header="response", message={"header": "Valve data", "Status": "Success", "Type": valve_type, "Location": valve_location, "State": value, "Actuation type": actuation_type, "Actuation priority": actuation_priority, "Last actuated": timestamp})
        enqueue(self.flag, log, LogPriority.INFO)


    def progress(self):
        self.flag.put(("general", "progress"), True)


    def test(self, msg: str):
        print("\ntest recieved:", msg)



"""
    def undo_soft_abort(self):
        # GO THROUGH EACH SENSOR AND CHECK STATUS
        sensor_list = self.registry.values["sensor_status"]
        critical_sensors = []
        for s_type in sensor_list:
            for s_loc in s_type:
                if sensor_list[s_type][s_loc] == LogPriority.CRIT:
                    critical_sensors.append([s_type, s_loc])
        
        # SEND FAILURE OR SUCCESS LOG DEPENDING ON CRITICAL VALUES FOUND/NOT FOUND
        if len(critical_sensors) > 0:
            log = Log(header="response", message={"header": "Soft abort cancellation", "Status": "Failure", "Description": "Soft abort cancellation unsuccessful - following sensors are still not safe: {}".format(critical_sensors)})
            enqueue(self.flag, log, LogPriority.CRIT)
        else:
            self.registry.put(("general", "soft_abort"), None)
            log = Log(header="response", message={"header": "Soft abort cancellation", "Status": "Success", "Description": "Soft abort successfully cancelled"})
            enqueue(self.flag, log, LogPriority.CRIT)
            enqueue(self.flag, Log(header="mode", message={"mode": "Normal"}), LogPriority.CRIT)
"""

