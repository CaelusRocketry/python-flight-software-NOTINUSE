"""
DEPRICATED: DON'T USE THIS FILE ANYMORE
"""


from ..telemetry.logging import Log
import subprocess
import sys
import time

TOK_DEL, TYPE_DEL = " ", ":"  # Token and type delimiters

def ingest(log, sense, valv, ABORT, SOFT_ABORT):
    global sensors, valves
    sensors = sense
    valves = valv
    print("Incoming:", log.message)

    # A dictionary to hep cast all data appropriately
    types = {"int": int,
             "float": float,
             "str": str,
             }

    # Dictionary to convert fuction strings into fuction objects
    funcs = {
        "ABORT": {
            "hard": (hard_abort, valves),
            "soft": (soft_abort, valves)
        },
        "HEARTBEAT": {
            "At": (heartbeat,)
        },
        "core": {
            "ip": (get_ip,),
            "temp": (get_core_temp,),
            "speed": (get_core_speed,),
            "time": (get_time,),
            "cpu": (get_cpu,)
        },
        "sensor": {
            "data": (sensor_data,sensors)
        },
        "valve": {
            "actuate": (actuate_valve,)
        }
    }

    header = log.header
    tokens = log.message.split(TOK_DEL)
    cmd, args = tokens[0], tokens[1:]

    # Casts the values as the type of the object in order to send message as a string
    args = list(map(lambda x: types[x.split(TYPE_DEL)[0]](
        x.split(TYPE_DEL)[1]), args))

    # Attemps to run the fuction assocated with the header, otherwise returns an error
    print(log)
    if header in funcs:
        if cmd in funcs[header]:
            func = funcs[header][cmd][0]
            params = funcs[header][cmd][1:]
            return func(*params, *args)
            return funcs[header][cmd](*args)
        return Log(header="ERROR", message="Unknown command while ingesting packet: Header was {} and cmd was {}".format(header, cmd))
    return Log(header="ERROR", message="Unknown header while ingesting packet: Header was {}".format(header))


# TODO: Return only the information from these three methods, and have the caller package into a Log
# TODO: change Enqueue and other things into Enum

def get_ip():
    """ Core method - Returns a Log containing the ip of the pi. """
    return Log(header="RESPONSE", message="192.168.1.35")
    # return "Enqueue", Log(header="RESPONSE", message=(subprocess.getoutput("hostname -I").split()[1]))

def get_core_temp():
    """ Core method - Returns a Log containing the internal temperature of the pi. """
    msg = subprocess.getoutput("/opt/vc/bin/vcgencmd measure_temp")[5:]
    print("Message:", msg)
    return Log(header="RESPONSE", message=msg)

def get_core_speed():
    """ Core method - Returns a Log containing the clock speed of the pi """
    msg = subprocess.getoutput("lscpu | grep MHz").split()[3] + " MHz"
    return Log(header="RESPONSE", message=msg)

def get_time():
    """ Core method - Returns a log containing the system time of the pi """
    msg = time.strftime("%a %d-%m-%Y @ %H:%M:%S")
    return Log(header="RESPONSE", message=msg)

def get_cpu():
    """ Core method - Returns a log containing the cpu usage of the pi """
    msg = subprocess.getoutput("top -n1 | awk '/Cpu\(s\):/ {print $2}'")
    return Log(header="RESPONSE", message=msg)

def find_sensor(sensors, type, location):
    """
    Sensor method - Given a sensor location, returns the sensor object from the array
    TODO: Convert sensors into a dictionary
    """
    for sensor in sensors:
        if type == sensor.sensor_type() and location == sensor.location():
            return sensor
    return None

def sensor_data(sensors, type, location):
    """
    Sensor method - Returns the data of the sensor given a location
    TODO: Remove assert
    """
    sensor = find_sensor(sensors, type, location)
    assert sensor is not None
    return Log(
        header="RESPONSE", message=sensor.data, timestamp=timestamp, sender=sensor.name())

def find_valve(valves, id):
    """
    Valve method - Given a valve id, returns the value object from the array
    TODO: turn valves into dictionary
    """
    for valve in valves:
        if id == valve.id:
            return valve
    return None

def actuate_valve(valves, id, target, priority):
    """
    Valve method - Actuates the valve at a given proprity, return a Log to be enqueued
    """
    if ABORT:
        return Log(header="INFO", message="Could not actuate valve since hard abort has been called", sender="supervisor")
    valve = find_valve(valves, id)
    valve.actuate(target, priority)
    return Log(
        header="INFO", message="Actuated valve", sender="supervisor")

def heartbeat():
    """ Returns a heartbeat Log to show that the connection is alive """
    return Log(header="HEARTBEAT", message="Ok")

def hard_abort(valves):
    """ Runs the abort methods of all valves """
    global ABORT, SOFT_ABORT
    if ABORT == True and SOFT_ABORT == False:
        return Log(header="INFO", message="Calling hard abort even though the system has already hard aborted, ignoring command")
    ABORT = True
    SOFT_ABORT = False
    for valve in valves:
        valve.abort()
    return Log(
        header="INFO", message="Hard aborting now", sender="supervisor")

def soft_abort(valves):
    """ Runs the soft abort procedure """
    global ABORT, SOFT_ABORT
    # This basically means that a hard abort was previously called, so ground shouldn't be able to take back control
    if ABORT and not SOFT_ABORT:
        return Log(header="INFO", message="Hard abort was already called, so soft abort can't be called", sender="supervisor")
    # This basically means that a soft abort was previously called, so control is given back to ground
    if ABORT and SOFT_ABORT:
        ABORT = False
        SOFT_ABORT = False
        return Log(header="INFO", message="Soft abort is being retracted, ground station should have normal control now", sender="supervisor")
    else:
        # Calls the same abort procedure as hard_abort, but sets the SOFT_ABORT variable to true, allowing it to be undone if ground station wants to.
        ABORT = True
        SOFT_ABORT = True
        for valve in valves:
            valve.abort()
        return Log(header="INFO", message="Soft abort is going into action, call soft_abort again to retract it", sender="supervisor")
