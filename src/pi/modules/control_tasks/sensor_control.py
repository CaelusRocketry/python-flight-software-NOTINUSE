import time
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.lib.packet import Log, LogPriority
from modules.lib.enums import SensorType, SensorLocation, SensorStatus

class SensorControl():
    def __init__(self, registry: Registry, flag: Flag):
        print("Sensor control")
        self.registry = registry
        self.flag = flag


    def begin(self, config: dict):
        self.config = config
        self.sensors = config["sensors"]["list"]
        self.boundaries = config["boundaries"]
        self.valves = config["valves"]["list"]
        self.send_interval = self.config["sensors"]["send_interval"]
        self.last_send_time = None
        self.kalman_args = config["kalman_args"]
        self.kalman_filters = config["kalman_setup"]
        for sensor_type in self.kalman_filters:
            for sensor_location in self.kalman_filters[sensor_type]:
                args = self.kalman_args[sensor_type][sensor_location]
                self.kalman_filters[sensor_type][sensor_location] = Kalman(args["process_variance"],
                                                                           args["measurement_variance"],
                                                                           args["kalman_value"])


    # Test to make sure sensor values aren't outside the boundaries set in the config. If they are, update the registry with the appropriate SensorStatus.
    def control(self):
       for sensor_type in self.sensors:
            for sensor_location in self.sensors[sensor_type]:
                _, val, _ = self.registry.get(("sensor", sensor_type, sensor_location))
                kalman_val = None
                filter = self.kalman_filters[sensor_type][sensor_location]
                if len(filter.sensor_value_list) >= 2 and val == filter.sensor_value_list[-1] and filter.sensor_value_list[-1] != filter.sensor_value_list[-2]:
                    kalman_val = filter.kalman_value_list[-1]
                else:
                    kalman_val = filter.update_kalman(val)
                if self.boundaries[sensor_type][sensor_location]["safe"][0] <= kalman_val <= self.boundaries[sensor_type][sensor_location]["safe"][1]:
                    self.registry.put(("sensor_status", sensor_type, sensor_location), SensorStatus.SAFE)
                elif self.boundaries[sensor_type][sensor_location]["warn"][0] <= kalman_val <= self.boundaries[sensor_type][sensor_location]["warn"][1]:
                    self.registry.put(("sensor_status", sensor_type, sensor_location), SensorStatus.WARNING)
                else:
                    self.registry.put(("sensor_status", sensor_type, sensor_location), SensorStatus.CRITICAL)


    def send_sensor_data(self):
        message = {}
        for sensor_type in self.sensors:
            for sensor_location in self.sensors[sensor_type]:
                _, val, _ = self.registry.get(("sensor", sensor_type, sensor_location))
                kalman_val = None
                filter = self.kalman_filters[sensor_type][sensor_location]
                if len(filter.sensor_value_list) >= 2 and val == filter.sensor_value_list[-1] and filter.sensor_value_list[-1] != filter.sensor_value_list[-2]:
                    kalman_val = filter.kalman_value_list[-1]
                else:
                    kalman_val = filter.update_kalman(val)
                if sensor_type not in message:
                    message[sensor_type] = {}
                message[sensor_type][sensor_location] = kalman_val
        log = Log(header="sensor_data", message=message)
        _, enqueue = self.flag.get(("telemetry", "enqueue"))
        enqueue.append((log, LogPriority.INFO))
        self.flag.put(("telemetry", "enqueue"), enqueue)


    def execute(self):
        if self.last_send_time is None or time.time() - self.last_send_time > self.send_interval:
            self.send_sensor_data()
            self.last_send_time = time.time()

        #TODO: Do stuff with the SensorStatuses here


class Kalman:

	def __init__(self, process_variance, measurement_variance, kalman_value):
		self.process_variance = process_variance ** 2
		self.measurement_variance = measurement_variance ** 2
		self.kalman_value = kalman_value
		self.sensor_value = kalman_value
		self.P, self.K = 1.0, 1.0
		self.kalman_value_list = []
		self.sensor_value_list = []

	def update_kalman(self, sensor_value):
		self.P += self.process_variance
		self.K = self.P / (self.P + self.measurement_variance)
		self.kalman_value = self.K * sensor_value + (1 - self.K) * self.kalman_value
		self.P *= (1 - self.K)

		self.kalman_value_list.append(self.kalman_value)
		self.sensor_value_list.append(sensor_value)
		return self.kalman_value
