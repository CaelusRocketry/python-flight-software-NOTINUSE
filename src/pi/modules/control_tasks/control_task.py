from modules.mcl.flag import Flag
from modules.lib.helpers import enqueue
from modules.mcl.registry import Registry
from modules.lib.packet import Log, LogPriority
from modules.control_tasks.valve_control import ValveControl
from modules.control_tasks.stage_control import StageControl
from modules.control_tasks.sensor_control import SensorControl
from modules.control_tasks.telemetry_control import TelemetryControl

class ControlTask():
    def __init__(self, registry: Registry, flag: Flag, task_config: dict):
        print("Config control task is active")
        self.controls = []
        self.registry = registry
        self.flag = flag
        self.task_config = task_config
        if "telemetry" in task_config:
            self.controls.append(TelemetryControl(self.registry, self.flag))
        if "sensor" in task_config:
            self.controls.append(SensorControl(self.registry, self.flag))
        if "valve" in task_config:
            self.controls.append(ValveControl(self.registry, self.flag))
        if "stage" in task_config:
            self.controls.append(StageControl(self.registry, self.flag))

    def begin(self, config: dict):
        for ctrl in self.controls:
            ctrl.begin(config)
        enqueue(self.flag, Log(header="mode", message={"mode": "Normal"}), LogPriority.CRIT)


    def control(self):
        for ctrl in self.controls:
            ctrl.execute()
