from modules.mcl.flag import Flag
from modules.mcl.registry import Registry
from modules.lib.enums import *
from modules.lib.errors import *
import json

class Telemetry_Control(): 
    def __init__(self):
        pass

    def ingest(self, state_field_registry: Registry, flags: Flag) -> PacketError: 
        telem_queue = state_field_registry.get(("telemetry", "ingest_queue"))
        funcs = {
            "hard_abort": (self.hard_abort, valves, flags),
            "soft_abort": (self.soft_abort, valves, flags),
            "valve_actuate_override": (self.valve_actuate_override, valve, location, actuation_type, value, flags),
            "solenoid_actuate": (self.solenoid_actuate, location, actuation_type, value, flags),
            "ball_actuate": (self.ball_actuate, location, value, flags),
            "sensor_request": (self.sensor_request, sensor, location, flags),
            "valve_request": (self.valve_request, valve, location, flags),
            "progress": (self.progress, stage, flags)
        }

        for packet in telem_queue:
            header = packet.header
            if header in funcs:
                func = funcs[header]
                packet_dict = json.loads(packet.to_string())
                packet_dict.pop("logs")
                args = packet_dict.values()
                func(*args)
            else:
                return PacketError.INVALID_HEADER_ERROR

        state_field_registry.put(("telemetry", "ingest_queue"), [])


    def hard_abort(self, valves: list, flags: Flag):
        flags.put(("abort", "hard_abort"), valves)


    def soft_abort(self, valves: list, flags: Flag):
        flags.put(("abort", "soft_abort"), valves)

    def valve_actuate_override(self, valve: ValveType, location: ValveLocation, actuation_type: ActuationType, value, flags: Flag) -> ValveActuationError:
        actuations = {
            ValveType.BALL: {
                ValveLocation.PRESSURE_RELIEF: {
                    ActuationType.PULSE: "ball_valve_pressure_relief_pulse",
                    ActuationType.OPEN_VENT: "ball_valve_pressure_relief_open_vent",
                    ActuationType.CLOSE_VENT: "ball_valve_pressure_relief_close_vent"
                },
                ValveLocation.PROPELLANT_VENT: {
                    ActuationType.PULSE: "ball_valve_propellant_vent_pulse",
                    ActuationType.OPEN_VENT: "ball_valve_propellant_vent_open_vent",
                    ActuationType.CLOSE_VENT: "ball_valve_propellant_vent_close_vent"
                },
                ValveLocation.MAIN_PROPELLANT_VALVE: {
                    ActuationType.PULSE: "ball_valve_main_propellant_valve_pulse",
                    ActuationType.OPEN_VENT: "ball_valve_main_propellant_valve_open_vent",
                    ActuationType.CLOSE_VENT: "ball_valve_main_propellant_valve_close_vent"
                }
            },
            ValveType.SOLENOID: {
                ValveLocation.PRESSURE_RELIEF: {
                    ActuationType.PULSE: "solenoid_valve_pressure_relief_pulse",
                    ActuationType.OPEN_VENT: "solenoid_valve_pressure_relief_open_vent",
                    ActuationType.CLOSE_VENT: "solenoid_valve_pressure_relief_close_vent"
                },
                ValveLocation.PROPELLANT_VENT: {
                    ActuationType.PULSE: "solenoid_valve_propellant_vent_pulse",
                    ActuationType.OPEN_VENT: "solenoid_valve_propellant_vent_open_vent",
                    ActuationType.CLOSE_VENT: "solenoid_valve_propellant_vent_close_vent"
                },
                ValveLocation.MAIN_PROPELLANT_VALVE: {
                    ActuationType.PULSE: "solenoid_valve_main_propellant_valve_pulse",
                    ActuationType.OPEN_VENT: "solenoid_valve_main_propellant_valve_open_vent",
                    ActuationType.CLOSE_VENT: "solenoid_valve_main_propellant_valve_close_vent"
                }
            }
        }

        if valve not in actuations:
            return ValveActuationError.VALVE_TYPE_ERROR
        elif location not in actuations[valve]:
            return ValveActuationError.LOCATION_ERROR
        elif actuation_type not in actuations[valve][location]:
            return ValveActuationError.ACTUATION_TYPE_ERROR
            
        if valve == ValveType.BALL:
            if not isinstance(value, int):
                return ValveActuationError.ACTUATION_VALUE_ERROR
            flags.put(("ball_valve_actuate", actuations[valve][location][actuation_type]), value)
        else:
            if not isinstance(value, bool):
                return ValveActuationError.ACTUATION_VALUE_ERROR
            flags.put(("solenoid_valve_actuate", actuations[valve][location][actuation_type]), value)


    def solenoid_actuate(self, location: ValveLocation, actuation_type: ActuationType, value: bool, flags: Flag) -> ValveActuationError:
        actuations = {
            ValveLocation.PRESSURE_RELIEF: {
                ActuationType.PULSE: "solenoid_valve_pressure_relief_pulse",
                ActuationType.OPEN_VENT: "solenoid_valve_pressure_relief_open_vent",
                ActuationType.CLOSE_VENT: "solenoid_valve_pressure_relief_close_vent"
            },
            ValveLocation.PROPELLANT_VENT: {
                ActuationType.PULSE: "solenoid_valve_propellant_vent_pulse",
                ActuationType.OPEN_VENT: "solenoid_valve_propellant_vent_open_vent",
                ActuationType.CLOSE_VENT: "solenoid_valve_propellant_vent_close_vent"
            },
            ValveLocation.MAIN_PROPELLANT_VALVE: {
                ActuationType.PULSE: "solenoid_valve_main_propellant_valve_pulse",
                ActuationType.OPEN_VENT: "solenoid_valve_main_propellant_valve_open_vent",
                ActuationType.CLOSE_VENT: "solenoid_valve_main_propellant_valve_close_vent"
            }
        }

        if location not in actuations:
            return ValveActuationError.LOCATION_ERROR
        elif actuation_type not in actuations[location]:
            return ValveActuationError.ACTUATION_TYPE_ERROR

        flags.put(("solenoid_valve_actuate", actuations[location][actuation_type]), value)


    def ball_actuate(self, location: ValveLocation, value: int, flags: Flag) -> ValveActuationError:
        actuations = {
            ValveLocation.PRESSURE_RELIEF: {
                ActuationType.PULSE: "ball_valve_pressure_relief_pulse",
                ActuationType.OPEN_VENT: "ball_valve_pressure_relief_open_vent",
                ActuationType.CLOSE_VENT: "ball_valve_pressure_relief_close_vent"
            },
            ValveLocation.PROPELLANT_VENT: {
                ActuationType.PULSE: "ball_valve_propellant_vent_pulse",
                ActuationType.OPEN_VENT: "ball_valve_propellant_vent_open_vent",
                ActuationType.CLOSE_VENT: "ball_valve_propellant_vent_close_vent"
            },
            ValveLocation.MAIN_PROPELLANT_VALVE: {
                ActuationType.PULSE: "ball_valve_main_propellant_valve_pulse",
                ActuationType.OPEN_VENT: "ball_valve_main_propellant_valve_open_vent",
                ActuationType.CLOSE_VENT: "ball_valve_main_propellant_valve_close_vent"
            }
        }

        if location not in actuations:
            return ValveActuationError.LOCATION_ERROR
        elif actuation_type not in actuations[location]:
            return ValveActuationError.ACTUATION_TYPE_ERROR

        flags.put(("ball_valve_actuate", actuations[location][actuation_type]), value)


    def sensor_request(self, sensor: SensorType, location: SensorLocation, flags: Flag) -> SensorRequestError:
        sensors = {
            SensorType.THERMOCOUPLE: {
                SensorLocation.CHAMBER: "thermocouple_chamber",
                SensorLocation.TANK: "thermocouple_tank",
            },
            SensorType.PRESSURE: {
                SensorLocation.CHAMBER: "pressure_chamber",
                SensorLocation.TANK: "pressure_tank",
                SensorLocation.INJECTOR: "pressure_injector"
            },
            SensorType.LOAD: {
                SensorLocation.TANK: "load_tank",
            }   
        }

        if sensor not in sensors:
            return SensorRequestError.SENSOR_TYPE_ERROR
        elif location not in sensors[sensor]:
            return SensorRequestError.SENSOR_LOCATION_ERROR

        flags.put(("sensor_request", sensors[sensor][location]), True)


    def valve_request(self, valve: ValveType, location: ValveLocation, flags: Flag) -> ValveRequestError: 
        valves = {
            ValveType.SOLENOID: {
                ValveLocation.PRESSURE_RELIEF: "solenoid_valve_pressure_relief",
                ValveLocation.PROPELLANT_VENT: "solenoid_valve_propellant_vent",
                ValveLocation.MAIN_PROPELLANT_VALVE: "solenoid_valve_main_propellant_valve"
            },
            ValveType.BALL: {
                ValveLocation.PRESSURE_RELIEF: "ball_valve_pressure_relief",
                ValveLocation.PROPELLANT_VENT: "ball_valve_propellant_vent",
                ValveLocation.MAIN_PROPELLANT_VALVE: "ball_valve_main_propellant_valve"
            }
        }

        if valve not in valves:
            return ValveRequestError.VALVE_TYPE_ERROR
        elif location not in valves[valve]:
            return ValveRequestError.VALVE_LOCATION_ERROR

        flags.put(("valve_request", valves[valve][location]), True)


    def progress(self, stage: Stage, flags: Flag):
        flags.put(("progress", "stage"), stage)

