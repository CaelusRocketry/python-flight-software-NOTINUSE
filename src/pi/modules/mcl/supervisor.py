### Import the necessary classes
import time
from modules.mcl.flag import Flag
from modules.mcl.registry import Registry
from modules.tasks.telemetry_task import TelemetryTask
from modules.tasks.sensor_task import SensorTask
from modules.tasks.valve_task import ValveTask
from modules.control_tasks.control_task import ControlTask
from modules.lib.enums import SensorType, SensorLocation, ValveType, ValveLocation

class Supervisor:

    def __init__(self, task_config: "dict", config: "dict"):
        self.task_config = task_config
        self.config = config
        self.parse_config()
        self.flag = Flag(self.config)
        self.registry = Registry(self.config)
        self.create_tasks()
    

    # Convert the strings in config to their respective enums (for both sensors and valves)
    def parse_config(self):
        sensor_dict = {"thermocouple": SensorType.THERMOCOUPLE, "pressure": SensorType.PRESSURE, "load": SensorType.LOAD}
        sensor_loc_dict = {"PT-1": SensorLocation.PT1, "PT-2": SensorLocation.PT2}
        valve_dict = {"solenoid": ValveType.SOLENOID, "ball": ValveType.BALL}
        valve_loc_dict = {"pressure_relief": ValveLocation.PRESSURE_RELIEF, "pressurization": ValveLocation.PRESSURIZATION, "main_propellant_valve": ValveLocation.MAIN_PROPELLANT_VALVE}
        sensor_config, valve_config = self.config["sensors"]["list"], self.config["valves"]["list"]
        sensors, valves = {}, {}

        for sensor in sensor_config:
            assert(sensor in sensor_dict)
            sensor = sensor_dict[sensor]
            sensors[sensor] = {}
            locs = sensor_config[sensor]
            for loc in locs:
                assert(loc in sensor_loc_dict)
                loc = sensor_loc_dict[loc]
                sensors[sensor][loc] = sensor_config[sensor][loc]

        for valve in valve_config:
            assert(valve in valve_dict)
            valve = valve_dict[valve]
            valves[valve] = {}
            locs = valve_config[valve]
            for loc in locs:
                assert(loc in valve_loc_dict)
                loc = valve_loc_dict[loc]
                valves[valve][loc] = valve_config[valve][loc]

        #FIXME: Currently overwriting, is this a good idea?
        self.sensors, self.valves = sensors, valves
        self.config["sensors"]["list"] = self.sensors
        self.config["valves"]["list"] = self.valves


    def create_tasks(self):
        tasks = []
        if "telemetry" in self.task_config["tasks"]:
            tasks.append(TelemetryTask(self.registry, self.flag))
        if "sensor" in self.task_config["tasks"]:
            tasks.append(SensorTask(self.registry, self.flag))
        if "valve" in self.task_config["tasks"]:
            tasks.append(ValveTask(self.registry, self.flag))

        self.tasks = tasks
        self.control_task = ControlTask(self.registry, self.flag, self.task_config["control_tasks"])
        self.control_task.begin(self.config)


    def initialize(self):
        for task in self.tasks:
            task.begin(self.config)
        self.control_task.begin(self.config)


    def read(self):
        for task in self.tasks:
            task.read()


    def control(self):
        self.control_task.control()


    def actuate(self):
        for task in self.tasks:
            task.actuate()


    def run(self):
        self.initialize()
        while True:
            self.read()
            self.control()
            self.actuate()
