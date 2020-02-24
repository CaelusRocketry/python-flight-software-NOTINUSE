from modules.tasks.telemetry_task import TelemetryTask
from modules.control_tasks.control_task import ControlTask
from modules.mcl.supervisor import Supervisor
import json

telemetry = TelemetryTask()
control = ControlTask()
config = json.loads(open("config.json").read())
supervisor = Supervisor(tasks=[telemetry], control_task=control, config=config)
supervisor.run()