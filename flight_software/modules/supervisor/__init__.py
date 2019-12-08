# /modules/supervisor

from threading import Thread
import time
import heapq
from ..telemetry.telemetry import Telemetry
from ..telemetry.logging import Packet, Log
from ..telemetry.encryption import decrypt
from ..sensors import SensorStatus
from ..sensors.thermocouple import Thermocouple
from ..sensors.imu import IMU
from ..sensors.force import Load
from ..valve import ValveType, Valve
#from .ingest import *

GS_IP = '192.168.1.29' 
GS_PORT = 5005
SENSOR_DELAY = 1.5

# Initialize all sensors
sensors = [
    Thermocouple(0, 0, "chamber"),
#    IMU("nose"),
#    Load(6, 5, "fuel")
]

# Initialize all valves
global valves
valves = [
    Valve(0, ValveType.Ball, 4, 17)
]

global ABORT, SOFT_ABORT
ABORT = False
SOFT_ABORT = False

# Initializes anything in the telemetry object and ingests it
def handle_telem(telem):
    telem.begin()  # Starts a sending and recieving thread, with associated queue_ingest and queue_send methods
    while True: 
        if not telem.queue_ingest.empty():  # if there is a message, begin a thread to interperate the message
            data = telem.queue_ingest.popleft()
            ingest_thread = Thread(target=interpret, args=(telem, data))
            ingest_thread.daemon = True
            ingest_thread.start()

# Handles the information returned by ingest
def interpret(telem, data):
    pck_str = decrypt(data)
    pck = Packet.from_string(pck_str)  # Deserialize the packet
    pack = Packet(header='RESPONSE')
    for log in pck.logs:
        response = ingest(log, sensors, valves)  # Performs the action requested and returns a response
        if response.header == "Error":
            print("Error", response.message)
        pack.add(response)

    telem.enqueue(pack)
    return

#  The main supervisor loop. An infinite loop that collects data from all sensors and sends it to ground station.
def start():
    # Initalize telemetry object
    telem = Telemetry(GS_IP, GS_PORT)
    telem_thread = Thread(target=handle_telem, args=(telem,))
    telem_thread.daemon = True
    telem_thread.start()

    # Begin the checking method for all sensors
    for sensor in sensors:
        sensor_thread = Thread(target=sensor.check)
        sensor_thread.daemon = True
        sensor_thread.start()     

    # Begin the loop that collects sensor data, synthesizes it into a packet, and sends it to ground stations
    while True:
        # The packet stores data from all sensors for this iteration
        packet = Packet(
            header='DATA',
            logs=[],
            timestamp=time.time()
            )

        for sensor in sensors:
            # TODO: Handle sensor status by doing something
            status = sensor.status()
            sensor_data = {"raw":sensor.data, "normalized":sensor.normalized}
            if status != SensorStatus.Safe:
                t = threading.Thread(target = confirm_level, args=(sensor,))
                t.daemon = True
                t.start()
            log = Log(  
                message=sensor_data,
                level=status,
                timestamp=sensor.timestamp,
                sender=sensor.name())

            packet.add(log)
            if status == SensorStatus.Crit:
                # sensor_thread = Thread(target=confirm_level, args=(sensor,))
                # have confirm_level actually call abort methods
                log = Log(header="POTENTIAL ABORT", level=SensorStatus.Crit, message="Aborting because " + sensor.name() + " has a critical value")
                packet.add(log)
                hard_abort(valves)

        telem.enqueue(packet)
        time.sleep(SENSOR_DELAY)

def confirm_level(sensor):
    packet = Packet(
        header='ABORT MESSAGES',
        logs=[],
        timestamp=time.time()
    )

    highest_stat = SensorStatus.Crit

    for i in range(5):
        print(i)
            
        data = sensor.get_data()
        stat = SensorStatus.Safe
        for key in sensor.datatypes:
            
            if data[key] == None:
                stat = SensorStatus.Crit
                break
            
            if data[key] >= sensor.boundaries[key][SensorStatus.Safe][0] and data[key] <= sensor.boundaries[key][SensorStatus.Safe][1]:
                stat = min(SensorStatus.Safe, stat)
            elif data[key] >= sensor.boundaries[key][SensorStatus.Warn][0] and data[key] <= sensor.boundaries[key][SensorStatus.Warn][1]:
                stat = min(SensorStatus.Warn, stat)
            else:
                stat = min(SensorStatus.Crit, stat)
            print("stat:", stat)
        
        highest_stat = max(stat, highest_stat)
        print("highest stat:", highest_stat)
        time.sleep(1)

    if(highest_stat == SensorStatus.Crit):
        print("SENSOR STATUS - CRIT: CALL ALL ABORTS")
        # log = Log(header="NO ABORT", level=SensorStatus.Crit, message="Not aorting because " + sensor.name() + " no longer has critical values")
        # packet.add(log)
        # hard_abort(valves)
    elif(highest_stat == SensorStatus.Warn):
        print("SENSOR STATUS - WARNING: CONSIDER ABORTING")
        # log = Log(header="NO ABORT", level=SensorStatus.Crit, message="Not aorting because " + sensor.name() + " no longer has critical values")
        # packet.add(log)
        # hard_abort(valves)
    else:
        print("SENSOR STATUS - SAFE: WE ALL GUCCI")
        # log = Log(header="ABORT", level=SensorStatus.Crit, message="Aborting because " + sensor.name() + " has a critical value")
        # packet.add(log)
        # hard_abort(valves)


def ingest(log):
    global sensors, valves
    print("Incoming:", log.message)

    # A dictionary to hep cast all data appropriately
    types = {"int": int,
             "float": float,
             "str": str,
             }

    # Dictionary to convert fuction strings into fuction objects
    funcs = {
        "ABORT": {
            "hard": hard_abort,
            "soft": soft_abort
        },
        "HEARTBEAT": {
            "At": heartbeat
        },
        "core": {
            "ip": get_ip,
            "temp": get_core_temp,
            "speed": get_core_speed,
            "time": get_time,
            "cpu": get_cpu
        },
        "sensor": {
            "data": sensor_data
        },
        "valve": {
            "actuate": actuate_valve
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
#            func = funcs[header][cmd][0]
#            params = funcs[header][cmd][1:]
#            return func(*params, *args)
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
