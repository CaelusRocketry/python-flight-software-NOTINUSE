from modules.tasks.sensor_arduino_task import SensorArduinoTask
from modules.control_tasks.control_task import ControlTask
from modules.mcl.supervisor import Supervisor
import json

telemetry = SensorArduinoTask()
control = ControlTask()
config = json.loads(open("config.json").read())
config["telemetry_control"] = True
config["sensor_control"] = False
config["valve_control"] = False
supervisor = Supervisor(tasks=[telemetry], control_task=control, config=config)
supervisor.run()