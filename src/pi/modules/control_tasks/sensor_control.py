import time
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.lib.packet import Log, LogPriority
from modules.lib.errors import Error
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
                err, val, timestamp = self.registry.get(("sensor", sensor_type, sensor_location))
                assert(err == Error.NONE)
                if sensor_type not in message:
                    message[sensor_type] = {}
                message[sensor_type][sensor_location] = val
        log = Log(header="sensor_data", message=message)
        err, enqueue = self.flag.get(("telemetry", "enqueue"))
        assert(err == Error.NONE)
        enqueue.append((log, LogPriority.INFO))
        err = self.flag.put(("telemetry", "enqueue"), enqueue)
        assert(err == Error.NONE)


    def execute(self):
        if self.last_send_time is None or time.time() - self.last_send_time > self.send_interval:
            self.send_sensor_data()
            self.last_send_time = time.time()


        #TODO: Make these values correspond with the sensors, right now they're just random
        #TODO: Add in all sensors properly

        """

        if self.registry.get(("sensor", "thermocouple_chamber")) > 250:
            pass

        if self.registry.get(("sensor", "thermocouple_tank")) > 250:
            pass

        if self.registry.get(("sensor", "pressure_chamber")) > 250:
            pass

        if self.registry.get(("sensor", "pressure_tank")) > 250:
            pass

        if self.registry.get(("sensor", "pressure_injector")) > 250:
            pass

        """