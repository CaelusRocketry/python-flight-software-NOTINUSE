import threading
import time
import heapq
from modules.telemetry.tcp_socket import Telemetry
from modules.telemetry.packet import Packet
from modules.sensors.thermocouple import Thermocouple
from modules.sensors.imu import IMU
from modules.sensors.force import Load
from modules.sensors import ValveType
from modules.sensors.valve import Valve
from .ingest import ingest
from multiprocessing import Process

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
            ingest_thread = Process(target=interpret, args=(telem, data))
            ingest_thread.daemon = True
            ingest_thread.start()
#            ingest_thread.join()
#            ingest_thread = threading.Thread(target=interpret, args=(telem,data))
#            ingest_thread.daemon = True
#            ingest_thread.start()


def interpret(telem, data):
    response = ingest(data, sensors, valves)
    print(response)
    if response[0] == "Enqueue":
        telem.enqueue(response[1])
    elif response[0] == "Error":
        print("Erorr occured while ingesting packet:", response[1])
    return


def start():
    telem = Telemetry(GS_IP, GS_PORT)

    telem_thread = threading.Thread(target=handle_telem, args=(telem,))
    telem_thread.daemon = True
    telem_thread.start()

    # Begin the checking method for all sensors
    for sensor in sensors:
        sensor_thread = threading.Thread(target=sensor.check)
        sensor_thread.daemon = True
        sensor_thread.start()

    while True:
        for sensor in sensors:
            # TODO: Handle sensor status by doing something
            status = sensor.status()
            # Automatically add all sensor data to priority queue, might wanna
            # change this to adding only requested data
            data = sensor.data
            if sensor.data == {}:
                continue
            timestamp = sensor.timestamp
            packet = Packet(
                header='DATA',
                message=data,
                level=status,
                timestamp=timestamp,
                sender=sensor.name())
            telem.enqueue(packet)
        time.sleep(SENSOR_DELAY)
