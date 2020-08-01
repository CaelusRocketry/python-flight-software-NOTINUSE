from modules.mcl.supervisor import Supervisor
import json

config = json.loads(open("hardware_config.json").read())
controls = ["timer", "valve", "telemetry"]
tasks = ["valve", "telemetry"]
task_config = {"tasks": tasks, "control_tasks": controls}
supervisor = Supervisor(task_config=task_config, config=config)
supervisor.run()
