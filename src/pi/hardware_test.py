from modules.mcl.supervisor import Supervisor
import json

config = json.loads(open("hardware_config.json").read())
# controls = ["timer", "sensor", "telemetry"]
# tasks = ["sensor", "telemetry"]
# controls = ["timer", "sensor", "valve", "telemetry", "stage"]
controls = ["timer", "sensor", "valve", "telemetry"]
tasks = ["valve", "sensor", "telemetry"]
# controls = ["timer", "telemetry"]
# tasks = ["telemetry"]
task_config = {"tasks": tasks, "control_tasks": controls}
supervisor = Supervisor(task_config=task_config, config=config)
supervisor.run()
