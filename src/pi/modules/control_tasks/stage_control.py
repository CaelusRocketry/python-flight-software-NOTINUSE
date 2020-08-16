import time
from modules.mcl.flag import Flag
from modules.lib.packet import Log, LogPriority
from modules.lib.errors import Error
from modules.mcl.registry import Registry
from modules.lib.enums import Stage, ValveLocation, ActuationType, ValvePriority
from modules.lib.helpers import enqueue

AUTOSEQUENCE_DELAY = 5.0
POSTBURN_DELAY = 10.0

class StageControl:

    def __init__(self, registry: Registry, flag: Flag):
        self.registry = registry
        self.flag = flag
        self.request_time = None
        self.send_time = None
        self.start_time = time.time()
        self.actuated_autosequence = False
        self.actuated_postburn = False


    def begin(self, config: dict):
        self.stage_names = config["stages"]["list"]
        self.stages = [Stage(name) for name in self.stage_names]
        self.request_interval = config["stages"]["request_interval"]
        self.send_interval = config["stages"]["send_interval"]
        self.stage_idx = 0
        self.curr_stage = self.stages[0]
        self.registry.put(("general", "stage"), self.curr_stage)
        self.registry.put(("general", "stage_status"), 0.0)
    

    # Returns how much of the stage has been done
    def calculate_status(self) -> float:
        curr = time.time()
        if self.curr_stage == Stage.WAITING:
            return 100
        elif self.curr_stage == Stage.AUTOSEQUENCE:
            # NOTE: Autosequence delay is currently set to 5s
            if self.actuated_autosequence:
                return 100
            else:
                return min(((curr - self.start_time) / AUTOSEQUENCE_DELAY) * 100.0, 100.0)
        elif self.curr_stage == Stage.POSTBURN:
            # NOTE: For now just assuming it'll take 10s for everything to depressurize, TODO: Actually check the pressure and wait until the pressure goes down to 0
            return min(((curr - self.start_time) / POSTBURN_DELAY) * 100.0, 100.0)
        raise Exception("Unknown stage: {}".format(str(self.curr_stage)))


    def send_progression_request(self):
        if self.request_time is None or time.time() > self.request_time + self.request_interval:
            log = Log(header="response", message={"header": "Stage progression request", "Current stage": self.curr_stage, "Next stage": self.stages[self.stage_idx + 1]})
            enqueue(self.flag, log, LogPriority.CRIT)
            self.request_time = time.time()


    def send_data(self):
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

    # flags
    # valve actuations
    def stage_valve_control(self):
        curr = time.time()
        if self.curr_stage == Stage.WAITING:
            pass
        elif self.curr_stage == Stage.AUTOSEQUENCE:
            if curr - time.time() > AUTOSEQUENCE_DELAY and not self.actuated_autosequence:
                # Actuate valve
                mpv = ValveLocation.MAIN_PROPELLANT_VALVE
                self.flag.put(("solenoid", "actuation_type", mpv), ActuationType.OPEN_VENT)
                self.flag.put(("solenoid", "actuation_priority", mpv), ValvePriority.PI_PRIORITY)
                self.actuated_autosequence = True
        elif self.curr_stage == Stage.POSTBURN:
            #TODO: Make sure this actuation is correct
            if not self.actuated_postburn:
                # Actuate valve
                for loc in ValveLocation:
                    self.flag.put(("solenoid", "actuation_type", loc), ActuationType.OPEN_VENT)
                    self.flag.put(("solenoid", "actuation_priority", loc), ValvePriority.PI_PRIORITY)
                self.actuated_postburn = True


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
        self.send_data()
