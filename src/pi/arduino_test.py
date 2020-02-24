from modules.tasks.sensor_arduino_task import SensorArduinoTask
from modules.mcl.supervisor import Supervisor
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
import time

arduino_task = SensorArduinoTask()
flag = Flag()
registry = Registry()


while True:
    arduino_task.read(registry, flag)
    time.sleep(1)

#supervisor = Supervisor([telemetry])
    