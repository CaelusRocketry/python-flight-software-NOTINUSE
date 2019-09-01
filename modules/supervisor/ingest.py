from modules.telemetry.packet import Packet
from modules.telemetry.encryption import decrypt
import subprocess
import sys
#from modules.supervisor import *

TOK_DEL, TYPE_DEL = " ", ":"

def ingest(encoded, sense, valv):
    global sensors, valves
    sensors = sense
    valves = valv
    packet_str = decrypt(encoded)
    pck = Packet.from_string(packet_str)
    print("Incoming:", pck.message)

    types = {"int": int,
             "float": float,
             "str": str,
            }

    funcs = {
        "ABORT": {
            "ABORT": abort,
        },
        "HEARTBEAT": {
            "At": heartbeat
        },
        "core": {
            "ip": get_ip,
            "temp": get_core_temp,
            "speed": get_core_speed
        },
        "sensor": {
            "data": sensor_data
        },
        "valve": {
            "actuate": actuate_valve
        }
    }

    header = pck.header
    tokens = pck.message.split(TOK_DEL)
    cmd, args = tokens[0], tokens[1:]

    args = list(map(lambda x: types[x.split(TYPE_DEL)[0]](x.split(TYPE_DEL)[1]), args))

    if header in funcs:
        if cmd in funcs[header]:
            return funcs[header][cmd](*args)
        return "Error", "Unknown command!"
    return "Error", "Unknown header!"


# Core methods

def get_ip():
    return "Enqueue", Packet(header="RESPONSE", message="192.168.1.35")
#    return(subprocess.getoutput("hostname -I").split()[1])

def get_core_temp():
    msg = subprocess.getoutput("/opt/vc/bin/vcgencmd measure_temp")[5:]
    return "Enqueue", Packet(header="RESPONSE", message=msg)

def get_core_speed():
    msg  = subprocess.getoutput("lscpu | grep MHz").split()[3]+" MHz"
    return "Enqueue", Packet(header="RESPONSE", message=msg)

# Sensor methods
def find_sensor(type, location):
    global sensors
    for sensor in sensors:
        if type == sensor.sensor_type() and location == sensor.location():
            return sensor
    return None

def sensor_data(type, location):
    sensor = find_sensor(type, location, sensors)
    assert sensor is not None
    return "Enqueue", Packet(header="RESPONSE", message=sensor.data, timestamp=timestamp, sender=sensor.name())

# Valve methods

def find_valve(id):
    global valves
    for valve in valves:
        if id == valve.id:
            return valve
    return None

def actuate_valve(id, target, priority):
    valve = find_valve(id)
    valve.actuate(target, priority)
    return "Enqueue", Packet(header="INFO", message="Actuated valve", sender="supervisor")

# Other methods

def heartbeat():
    return "Enqueue", Packet(header="HEARTBEAT", message="Ok")

def abort():
    ABORT = True
    for valve in valves:
        valve.abort()
    return "Enqueue", Packet(haeder="INFO", message="Aborting now", sender="supervisor")