# /modules/supervisor

from threading import Thread
import time
import heapq
from modules.telemetry.tcp_socket import Telemetry
from modules.telemetry.packet import Packet
from modules.sensors.thermocouple import Thermocouple
from modules.sensors.imu import IMU
from modules.sensors.force import Load
from modules.valve import ValveType, Valve
from .ingest import ingest

GS_IP = '192.168.1.75'
GS_PORT = 5005
ABORT = False
SENSOR_DELAY = 1.5

sensors = [
    Thermocouple(0, 0, "chamber"),
    IMU("nose"),
    Load(6, 5, "fuel")
]

valves = [
    Valve(0, ValveType.Ball, 4, 17)
]


def handle_telem(telem):
    telem.begin()
    while True:
        if telem.queue_ingest:
            data = telem.queue_ingest.popleft()
            ingest_thread = Thread(target=interpret, args=(telem, data))
            ingest_thread.daemon = True
            ingest_thread.start()

def interpret(telem, data):
    response = ingest(data, sensors, valves)
    if response[0] == "Enqueue":
        print("Enqueuing", len(telem.queue_send), response[1])
        telem.enqueue(response[1])
    elif response[0] == "Error":
        print("Error occured while ingesting packet:", response[1])
    return


def start():
    telem = Telemetry(GS_IP, GS_PORT)

    telem_thread = Thread(target=handle_telem, args=(telem,))
    telem_thread.daemon = True
    telem_thread.start()
#    handle_telem(telem)

    # Begin the checking method for all sensors
    for sensor in sensors:
        sensor_thread = Thread(target=sensor.check)
        sensor_thread.daemon = True
        sensor_thread.start()

    while True:
        packet_data = {}
        for sensor in sensors:
            # TODO: Handle sensor status by doing something
            status = sensor.status()
            # Automatically add all sensor data to priority queue, might wanna
            # change this to adding only requested data
            data = sensor.data
            if sensor.data == {}:
                continue
            timestamp = sensor.timestamp
            packet_data[sensor.name] = data
#            telem.enqueue(packet)
        packet = Packet(
            header='DATA',
            message=packet_data,
            level=status,
            timestamp=time.time(),
            sender="Flight Pi")
        time.sleep(SENSOR_DELAY)
