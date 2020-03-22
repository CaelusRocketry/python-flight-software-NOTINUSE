import time
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.lib.packet import Log, LogPriority
from modules.lib.enums import SensorType, SensorLocation

class SensorControl():
    def __init__(self, registry: Registry, flag: Flag):
        print("Sensor control")
        self.registry = registry
        self.flag = flag


    def begin(self, config: dict):
        self.config = config
        self.sensors = config["sensors"]["list"]
        self.valves = config["valves"]["list"]
        self.send_interval = self.config["sensors"]["send_interval"]
        self.last_send_time = None


    def send_sensor_data(self):
        message = {}
        for sensor_type in self.sensors:
            for sensor_location in self.sensors[sensor_type]:
                _, val, timestamp = self.registry.get(("sensor", sensor_type, sensor_location))
                if sensor_type not in message:
                    message[sensor_type] = {}
                message[sensor_type][sensor_location] = val
        log = Log(header="sensor_data", message=message)
        _, enqueue = self.flag.get(("telemetry", "enqueue"))
        enqueue.append((log, LogPriority.INFO))
        self.flag.put(("telemetry", "enqueue"), enqueue)


    def execute(self):
        if self.last_send_time is None or time.time() - self.last_send_time > self.send_interval:
            self.send_sensor_data()
            self.last_send_time = time.time()

        #TODO: Make these values correspond with the sensors, right now they're just random
        #TODO: Add in all sensors properly

        if self.registry.get(("sensor_kalman", "thermocouple", "chamber")) > 250:
            pass

        if self.registry.get(("sensor_kalman", "thermocouple", "tank")) > 250:
            pass

        if self.registry.get(("sensor_kalman", "pressure", "chamber")) > 250:
            pass

        if self.registry.get(("sensor_kalman", "pressure", "tank")) > 250:
            pass

        if self.registry.get(("sensor_kalman", "pressure", "injector")) > 250:
            pass
