from modules.tasks.telemetry_task import TelemetryTask
from modules.control_tasks.control_task import ControlTask
from modules.mcl.supervisor import Supervisor
import json

config = json.loads(open("config.json").read())
config["telemetry_control"] = True
config["sensor_control"] = False
config["valve_control"] = False
telemetry = TelemetryTask()
control = ControlTask()
control.begin(config)
supervisor = Supervisor(tasks=[telemetry], control_task=control, config=config)
supervisor.run()