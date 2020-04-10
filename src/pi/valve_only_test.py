import json
from modules.mcl.supervisor import Supervisor

config = json.loads(open("config.json").read())
controls = ["valve"]
tasks = ["valve"]
task_config = {"tasks": tasks, "control_tasks": controls}
supervisor = Supervisor(task_config=task_config, config=config)
supervisor.run()