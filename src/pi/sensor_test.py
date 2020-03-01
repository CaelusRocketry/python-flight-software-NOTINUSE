import json
from modules.mcl.supervisor import Supervisor
from modules.control_tasks.control_task import ControlTask
from modules.tasks.sensor_arduino_task import SensorArduinoTask

config = json.loads(open("config.json").read())
config["telemetry_control"] = False
config["sensor_control"] = True
config["valve_control"] = False
sensor = SensorArduinoTask()
control = ControlTask()
supervisor = Supervisor(tasks=[sensor], control_task=control, config=config)
supervisor.run()