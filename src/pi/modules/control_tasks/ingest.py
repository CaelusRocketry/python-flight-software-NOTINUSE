from enum import Enum


def ingest(self, telem_queue):
    funcs = {
        "hard_abort": (hard_abort, valves),
        "soft_abort": (soft_abort, valves),
        "valve_actuate_override": (valve_actuate_override, valve, location, actuation_type, value),
        "solenoid_actuate": (solenoid_actuate, location, actuation_type, value),
        "ball_actuate": (ball_actuate, location, value),
        "sensor_request": (sensor_request, sensor, location),
        "valve_request": (valve_request, valve, location),
        "progress": (progress, stage)
    }

    for i in telem_queue:
        header = i.header
        if header in funcs:
            func = funcs[header]
            args = i.data.values()
            func(*args)


def hard_abort(valves):
    pass


def soft_abort(valves):
    pass


def valve_actuate_override(valve, location, actuation_type, value):
    pass


def solenoid_actuate(location, actuation_type, value):
    pass


def ball_actuate(location, value):
    pass


def sensor_request(sensor, location):
    pass


def valve_request(valve, location):
    pass


def progress(stage):
    pass


class SensorType(Enum):
    Thermocouple = 1
    Pressure = 2
    Load = 3


class SensorLocation(Enum):
    Chamber = 1
    Tank = 2
    Injector = 3


class SolenoidState(Enum):
    Open = 1
    Close = 2


class SensorStatus(Enum):
    Safe = 1
    Warning = 2
    Critical = 3


class ValveType(Enum):
    Solenoid = 1
    Ball = 2


class ValveLocation(Enum):
    PressureRelief = 1
    PropellantVent = 2
    MainPropellantValve = 3


class ActuationType(Enum):
    Pulse = 1
    OpenVent = 2
    CloseVent = 3


class Stage(Enum):
    PropellantLoading = 1
    LeakTesting1 = 2
    PressurantLoading = 3
    LeakTesting2 = 4
    PreIgnition = 5
    Disconnection = 6
