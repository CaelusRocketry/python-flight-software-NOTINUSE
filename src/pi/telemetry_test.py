from modules.tasks.telemetry_task import TelemetryTask
from modules.control_tasks.control_task import ControlTask
from modules.mcl.supervisor import Supervisor
import json

config = json.loads(open("config.json").read())
controls = ["telemetry"]
tasks = ["sensor", "telemetry"]
task_config = {"tasks": tasks, "control_tasks": controls}
supervisor = Supervisor(task_config=task_config, config=config)
supervisor.run()