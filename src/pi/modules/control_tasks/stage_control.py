import time
from modules.mcl.flag import Flag
from modules.lib.packet import Log, LogPriority
from modules.lib.errors import Error
from modules.mcl.registry import Registry
from modules.lib.enums import Stage
from modules.lib.helpers import enqueue

class StageControl:

    def __init__(self, registry: Registry, flag: Flag):
        self.registry = registry
        self.flag = flag
        self.request_time = None
        self.send_time = None
        self.start_time = time.time()
    

    def begin(self, config: dict):
        self.stage_names = config["stages"]["list"]
        self.stages = [Stage(name) for name in self.stage_names]
        self.request_interval = config["stages"]["request_interval"]
        self.send_interval = config["stages"]["send_interval"]
        self.stage_idx = 0
        self.curr_stage = self.stages[0]
        self.registry.put(("general", "stage"), self.curr_stage)
        self.registry.put(("general", "stage_status"), 0.0)
    

    def calculate_status(self) -> float:
        #TODO: Implement actual calculations for this kinda stuff
        if self.curr_stage == Stage.PROPELLANT_LOADING:
            pass
        elif self.curr_stage == Stage.LEAK_TESTING_1:
            pass
        elif self.curr_stage == Stage.PRESSURANT_LOADING:
            pass
        elif self.curr_stage == Stage.LEAK_TESTING_2:
            pass
        elif self.curr_stage == Stage.PRE_IGNITION:
            pass
        elif self.curr_stage == Stage.DISCONNECTION:
            pass

        return min((time.time() - self.start_time) * 5, 100.0)


    def send_progression_request(self):
        if self.request_time is None or time.time() > self.request_time + self.request_interval:
            log = Log(header="response", message={"header": "Stage progression request", "Current stage": self.curr_stage, "Next stage": self.stages[self.stage_idx + 1]})
            enqueue(self.flag, log, LogPriority.CRIT)
            self.request_time = time.time()


    def send_stage_data(self):
        if self.send_time is None or time.time() > self.send_time + self.send_interval:
            log = Log(header="stage", message={"stage": self.curr_stage, "status": self.status})
            enqueue(self.flag, log, LogPriority.INFO)
            self.send_time = time.time()


    def progress(self):
        if self.status != 100:
            log = Log(header="response", message={"header": "Stage progression failed", "description": "Stage progression failed, rocket not yet ready", "Stage": self.curr_stage, "Status": self.status})
            enqueue(self.flag, log, LogPriority.CRIT)
            return

        self.stage_idx += 1
        self.curr_stage = self.stages[self.stage_idx]
        self.registry.put(("general", "stage"), self.curr_stage)
        self.send_time = None
        self.request_time = None
        self.status = self.calculate_status()
        self.registry.put(("general", "stage_status"), self.status)
        self.start_time = time.time()
        log = Log(header="response", message={"header": "Stage progression successful", "description": "Stage progression was successful", "Stage": self.curr_stage, "Status": self.status})
        enqueue(self.flag, log, LogPriority.CRIT)


    def stage_valve_control(self):
        # TODO: Actuate valves, make sure they're actuated properly
        # Valve actuation should depend on current stage, so do it in a switch statement
        pass


    def execute(self):
        self.status = self.calculate_status()
        self.registry.put(("general", "stage_status"), self.status)
        _, progress = self.flag.get(("general", "progress"))
        if progress:
            self.progress()
            self.flag.put(("general", "progress"), False)
        elif self.status == 100:
            self.send_progression_request()

        self.stage_valve_control()
        self.send_stage_data()
