from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.control_tasks.sensor_control import SensorControl
from modules.control_tasks.telemetry_control import TelemetryControl
from modules.control_tasks.valve_control import ValveControl

class ControlTask():
    def __init__(self, registry: Registry, flag: Flag):
        print("Config control task is active")
        self.controls = []
        self.registry = registry
        self.flag = flag

    def begin(self, config: dict):
        self.config = config
        if "telemetry" in config:
            self.controls.append(TelemetryControl(self.registry, self.flag))
        if "sensor" in config:
            self.controls.append(SensorControl(self.registry, self.flag))
        if "valve" in config:
            self.controls.append(ValveControl(self.registry, self.flag))

    def control(self):
        for ctrl in self.controls:
            ctrl.execute()
