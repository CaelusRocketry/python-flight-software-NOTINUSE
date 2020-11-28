from modules.mcl.supervisor import Supervisor
import json
import argparse

def main():
    config = {}
    controls = []
    tasks = []
    
    parser = argparse.ArgumentParser(description='Run the Project Caelus Flight Software.', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--config', help="The config file to use for the simulation (enter " + 
            "local if you want to run the simulation on the default local config). \n" + 
            "Default: config.json")

    parser.add_argument('--tasks', metavar='Task', type=str, nargs='+',
            help="Space-separated list of tasks to run in the simulation.\n" + 
            "Available tasks: sensor, valve, telemetry\n" + 
            "Example: python main.py --tasks sensor valve\n" + 
            "Default: list of all available tasks")

    parser.add_argument('--control-tasks', metavar='ControlTask', type=str, nargs='+',
            help="Space-separated list of control tasks to run in the simulation.\n" + 
            "Available control tasks: sensor, valve, telemetry, pressure, stage, timer\n" + 
            "Example: python main.py --control-tasks sensor valve telemetry\n" + 
            "Default: list of all available control tasks")

    args = parser.parse_args()

    if args.config == "local":
        config = json.loads(open("config.json").read())
        config["telemetry"]["GS_IP"] = "127.0.0.1"
        config["telemetry"]["SOCKETIO_HOST"] = "127.0.0.1"
        config["arduino_type"] = "pseudo"
    elif args.config != None:
        try:
            config = json.loads(open(args.config).read())
        except:
            raise Exception("Error reading from config file '" + args.config + "'")
    else:
        config = json.loads(open("config.json").read())

    if args.tasks != None:
        tasks = args.tasks
    else:
        tasks = ["sensor", "valve", "telemetry"]

    if args.control_tasks != None:
        control_tasks = args.control_tasks
    else:
        control_tasks = ["sensor", "valve", "telemetry", "timer", "pressure", "stage"]
 
    task_config = {"tasks": tasks, "control_tasks": control_tasks}

    supervisor = Supervisor(task_config=task_config, config=config)
    supervisor.run()

if __name__ == "__main__":
    main()

