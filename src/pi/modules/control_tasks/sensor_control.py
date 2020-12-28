import time
from modules.mcl.flag import Flag
from modules.lib.kalman import Kalman
from modules.lib.helpers import enqueue
from modules.mcl.registry import Registry
from modules.lib.packet import Log, LogPriority
from modules.lib.enums import SensorType, SensorLocation, SensorStatus

class SensorControl():
    def __init__(self, registry: Registry, flag: Flag):
        print("Sensor control")
        self.registry = registry
        self.flag = flag


    def begin(self, config: dict):
        self.config = config
        sensor_config = config["sensors"]["list"]

        self.sensors = {}
        self.boundaries = {}
        self.kalman_args = {}
        for sensor_type in sensor_config:
            self.sensors[sensor_type] = []
            self.boundaries[sensor_type] = {}
            self.kalman_args[sensor_type] = {}
            for sensor_loc in sensor_config[sensor_type]:
                self.sensors[sensor_type].append(sensor_loc)
                self.boundaries[sensor_type][sensor_loc] = sensor_config[sensor_type][sensor_loc]["boundaries"]["waiting"]
                self.kalman_args[sensor_type][sensor_loc] =  sensor_config[sensor_type][sensor_loc]["kalman_args"]
        self.send_interval = self.config["sensors"]["send_interval"]
        self.last_send_time = None
        self.init_kalman(config)
    

    def init_kalman(self, config: dict):
        self.kalman_filters = {}
        for sensor_type in self.sensors:
            self.kalman_filters[sensor_type] = {}
            for sensor_location in self.sensors[sensor_type]:
                args = self.kalman_args[sensor_type][sensor_location]
                self.kalman_filters[sensor_type][sensor_location] = Kalman(args["process_variance"],
                                                                           args["measurement_variance"],
                                                                           args["kalman_value"])


    # Test to make sure sensor values aren't outside the boundaries set in the config. If they are, update the registry with the appropriate SensorStatus.
    def boundary_check(self):
        crits = []
        for sensor_type in self.sensors:
            for sensor_location in self.sensors[sensor_type]:
                _, val, _ = self.registry.get(("sensor_measured", sensor_type, sensor_location))
                kalman_val = self.kalman_filters[sensor_type][sensor_location].update_kalman(val)
                boundaries = self.boundaries[sensor_type][sensor_location]
                self.registry.put(("sensor_normalized", sensor_type, sensor_location), kalman_val)
                if boundaries["safe"][0] <= kalman_val <= boundaries["safe"][1]:
                    self.registry.put(("sensor_status", sensor_type, sensor_location), SensorStatus.SAFE)
                elif boundaries["warn"][0] <= kalman_val <= boundaries["warn"][1]:
                    self.registry.put(("sensor_status", sensor_type, sensor_location), SensorStatus.WARNING)
                else:
                    self.registry.put(("sensor_status", sensor_type, sensor_location), SensorStatus.CRITICAL)
                    crits.append([sensor_type, sensor_location])

        soft = self.registry.get(("general", "soft_abort"))[1]
        # if not hard:
        #     if len(crits) == 0 and soft:
        #         # TODO: Put hard_abort and soft_abort in flag?
        #         # Undo soft abort (since all sensors are back to normal)
        #         self.registry.put(("general", "soft_abort"), False)
        #         log = Log(header="response", message={"header": "Undoing soft abort", "Description": "All sensors have returned to non-critical levels"})
        #         enqueue(self.flag, log, LogPriority.CRIT)
        #         enqueue(self.flag, Log(header="mode", message={"mode": "Normal"}), LogPriority.CRIT)
        
        # executes soft abort
        if len(crits) > 0 and not soft:
                # soft abort if sensor status is critical and send info to GS
                self.registry.put(("general", "soft_abort"), True)
                log = Log(header="response", message={"header": "Soft abort", "Description": sensor_type + " in " + sensor_location + " reached critical levels"})
                enqueue(self.flag, log, LogPriority.CRIT)
                enqueue(self.flag, Log(header="mode", message={"mode": "soft abort"}), LogPriority.CRIT)

    def send_sensor_data(self):
        message = {}
        for sensor_type in self.sensors:
            message[sensor_type] = {}
            for sensor_location in self.sensors[sensor_type]:
                _, val, _ = self.registry.get(("sensor_measured", sensor_type, sensor_location))
                _, kalman_val, _ = self.registry.get(("sensor_normalized", sensor_type, sensor_location))
                _, status, _ = self.registry.get(("sensor_status", sensor_type, sensor_location))                
                message[sensor_type][sensor_location] = {"value": (val, kalman_val), "status": status}
        log = Log(header="sensor_data", message=message)
        enqueue(self.flag, log, LogPriority.INFO)


    def execute(self):
        self.boundary_check()
        if self.last_send_time is None or time.time() - self.last_send_time > self.send_interval:
            self.send_sensor_data()
            self.last_send_time = time.time()
#            print("Sending sensor data", time.time())
