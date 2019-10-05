from modules.telemetry.packet import Packet
from modules.telemetry.encryption import decrypt
import subprocess
import sys

TOK_DEL, TYPE_DEL = " ", ":"  # Token and type delimiters

#  
def ingest(encoded, sense, valv):
    global sensors, valves
    sensors = sense
    valves = valv
    packet_str = decrypt(encoded)
    pck = Packet.from_string(packet_str)  # Deserialize the packet
    print("Incoming:", pck.message)

    # A dictionary to hep cast all data appropriately
    types = {"int": int,
             "float": float,
             "str": str,
             }

    # Dictionary to convert fuction strings into fuction objects
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

    # Casts the values as the type of the object in order to send message as a string
    args = list(map(lambda x: types[x.split(TYPE_DEL)[0]](  
        x.split(TYPE_DEL)[1]), args))

    # Attemps to run the fuction assocated with the header, otherwise returns an error
    print(pck)
    if header in funcs:
        if cmd in funcs[header]:
            return funcs[header][cmd](*args)
        return "Error", "Unknown command!"
    return "Error", "Unknown header!"


# TODO: Return only the information from these three methods, and have the caller package into a Packet
# TODO: change Enqueue into Enum

# Core method - Returns a Packet containing the ip of the pi 
def get_ip():
    return "Enqueue", Packet(header="RESPONSE", message="192.168.1.35")
    # return "Enqueue", Packet(header="RESPONSE", message=(subprocess.getoutput("hostname -I").split()[1]))

# Core method - Returns a Packet containing the internal temperature of the pi
def get_core_temp():
    msg = subprocess.getoutput("/opt/vc/bin/vcgencmd measure_temp")[5:]
    print("Message:", msg)
    return "Enqueue", Packet(header="RESPONSE", message=msg)

# Core method - Returns a Packet containing the clock speed of the pi
def get_core_speed():
    msg = subprocess.getoutput("lscpu | grep MHz").split()[3] + " MHz"
    return "Enqueue", Packet(header="RESPONSE", message=msg)


# Sensor method - Given a sensor array, returns the sensor object at a certain location
# TODO: Convert sensors into a dictionary
def find_sensor(type, location):
    global sensors
    for sensor in sensors:
        if type == sensor.sensor_type() and location == sensor.location():
            return sensor
    return None

# Sensor method - 
def sensor_data(type, location):
    sensor = find_sensor(type, location, sensors)
    assert sensor is not None
    return "Enqueue", Packet(
        header="RESPONSE", message=sensor.data, timestamp=timestamp, sender=sensor.name())


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
    return "Enqueue", Packet(
        header="INFO", message="Actuated valve", sender="supervisor")


# Other methods

def heartbeat():
    return "Enqueue", Packet(header="HEARTBEAT", message="Ok")


def abort():
    ABORT = True
    for valve in valves:
        valve.abort()
    return "Enqueue", Packet(
        haeder="INFO", message="Aborting now", sender="supervisor")
