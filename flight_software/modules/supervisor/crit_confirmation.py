'''
file to check the confrm_level folder; now incorporated into __init__.py : delete?
'''

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

# Initialize all valves
global valves
valves = [
    Valve(0, ValveType.Ball, 4, 17)
]

therm = Thermocouple(0, 0, "chamber")
confirm_level(therm)

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
        for key in data:
            
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
        print("No crit status, so don't abort")
        # log = Log(header="ABORT", level=SensorStatus.Crit, message="Aborting because " + sensor.name() + " has a critical value")
        # packet.add(log)
        # hard_abort(valves)

    else:
        print("CRIT STATUS - CALL ALL ABORTS")
        # log = Log(header="NO ABORT", level=SensorStatus.Crit, message="Not aorting because " + sensor.name() + " no longer has critical values")
        # packet.add(log)
        # hard_abort(valves)