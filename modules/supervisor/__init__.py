import threading, time, heapq
from modules.telemetry.tcp_socket import Telemetry
from modules.telemetry.packet import Packet
from modules.sensors.thermocouple import Thermocouple
from .ingest import ingest

GS_IP = '127.0.0.1'
GS_PORT = 5005

def handle_telem(telem):
    telem.begin()
    while True:
        if telem.queue_ingest:
            data = telem.queue_ingest.popleft()
            ingest_thread = threading.Thread(target=interpret, args=(telem,data))
            ingest_thread.daemon = True
            ingest_thread.start()

def interpret(telem, data):
    response = ingest(data)
    print(response)
    if response[0] == "Enqueue":
        telem.enqueue(response[1])
    elif response[0] == "Error":
        print("Erorr occured while ingesting packet:", response[1])

def start():
    telem = Telemetry(GS_IP, GS_PORT)

    telem_thread = threading.Thread(target=handle_telem, args=(telem,))
    telem_thread.daemon = True
    telem_thread.start()

    sensors = [
        Thermocouple("nose"),
        Thermocouple("tank"),
        Thermocouple("chamber")
    ]

    #Begin the checking method for all sensors
    for sensor in sensors:
        sensor_thread = threading.Thread(target=sensor.check)
        sensor_thread.daemon = True
        sensor_thread.start()

    delay_time = .100
    while True:
        for sensor in sensors:
            #TODO: Handle sensor status by doing something
            status = sensor.status()
            # Automatically add all sensor data to priority queue, might wanna change this to adding only requested data
            data = sensor.data
            timestamp = sensor.timestamp
            packet = Packet(header='DATA', message=data, level=status, timestamp=timestamp)
            telem.enqueue(packet)
        time.sleep(delay_time)
