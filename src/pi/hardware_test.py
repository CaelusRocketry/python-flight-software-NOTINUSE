from modules.mcl.supervisor import Supervisor
import json

config = json.loads(open("hardware_config.json").read())
# controls = ["timer", "sensor", "telemetry"]
# tasks = ["sensor", "telemetry"]
# controls = ["timer", "sensor", "valve", "pressure"]
# tasks = ["sensor", "valve"]
controls = ["timer", "sensor", "valve", "pressure"]
tasks = ["sensor", "valve"]
task_config = {"tasks": tasks, "control_tasks": controls}
supervisor = Supervisor(task_config=task_config, config=config)
supervisor.run()
