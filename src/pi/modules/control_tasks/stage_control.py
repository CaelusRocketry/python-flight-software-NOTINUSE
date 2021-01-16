import time
from modules.mcl.flag import Flag
from modules.lib.packet import Log, LogPriority
from modules.lib.errors import Error
from modules.mcl.registry import Registry
from modules.lib.enums import Stage, ValveLocation, SensorLocation, ActuationType, ValvePriority, ValveType
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
        self.actuated_postburn = False


    def begin(self, config: dict):
        self.stage_names = config["stages"]["list"]
        self.stages = [Stage(name) for name in self.stage_names]
        self.request_interval = config["stages"]["request_interval"]
        self.send_interval = config["stages"]["send_interval"]
        self.sensors = config["sensors"]["list"]["pressure"]
        self.stage_idx = 0
        self.curr_stage = self.stages[0]
        self.registry.put(("general", "stage"), self.curr_stage)
        self.registry.put(("general", "stage_status"), 0.0)
    

    # Returns how much of the stage has been done
    def calculate_status(self) -> float:
        curr = time.time()
        if self.curr_stage == Stage.WAITING:
            return 100.0
        elif self.curr_stage == Stage.PRESSURIZATION:
            # TODO: If status == 100.0, don't decrease it
            # Target pressure for PT2 is 490 psi
            if SensorLocation.PT2.value in self.sensors:
                pressure = self.registry.get(("sensor_normalized", "pressure", SensorLocation.PT2))[1]
                return min(100.0, pressure / 4.9)
            else:
                return 100.0
        elif self.curr_stage == Stage.AUTOSEQUENCE:
            # NOTE: Autosequence delay is currently set to 5s
            mpv_actuation = self.registry.get(("valve_actuation", "actuation_type", ValveType.SOLENOID, ValveLocation.MAIN_PROPELLANT_VALVE))[1]
            if mpv_actuation == ActuationType.OPEN_VENT:
                return 100.0
            else:
                return min(((curr - self.start_time) / AUTOSEQUENCE_DELAY) * 100.0, 99.0)
        elif self.curr_stage == Stage.POSTBURN:
            # NOTE: Assuming that "depressurization" means 20psi
            if SensorLocation.PT2.value in self.sensors:
                pressure = self.registry.get(("sensor_normalized", "pressure", SensorLocation.PT2))[1]
                inv = (pressure - 20.0) / 5.0
                progress = min(100.0, 100.0 - inv)
                return max(0.0, progress) # makes sure that progress isnt negative
            else:
                return 100.0
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
        if self.status != 100 or self.registry.get(("general", "soft_abort"))[1]:
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
            for valve_loc in [ValveLocation.PRESSURIZATION_VALVE, ValveLocation.MAIN_PROPELLANT_VALVE]:
                actuation = self.registry.get(("valve_actuation", "actuation_type", ValveType.SOLENOID, valve_loc))[1]
                if actuation != ActuationType.CLOSE_VENT:
                    # print("CLOSING VALVE WITH PI_PRIORITY BC IN WAITING STAGE")
                    self.flag.put(("solenoid", "actuation_type", valve_loc), ActuationType.CLOSE_VENT)
                    self.flag.put(("solenoid", "actuation_priority", valve_loc), ValvePriority.PI_PRIORITY)
        elif self.curr_stage == Stage.PRESSURIZATION:
            pass
            # nv1_actuation = self.registry.get(("valve_actuation", "actuation_type", ValveType.SOLENOID, ValveLocation.PRESSURIZATION))[1]
            # if nv1_actuation != ActuationType.OPEN_VENT:
            #     self.flag.put(("solenoid", "actuation_type", ValveLocation.PRESSURIZATION), ActuationType.OPEN_VENT)
            #     self.flag.put(("solenoid", "actuation_priority", ValveLocation.PRESSURIZATION), ValvePriority.PI_PRIORITY)
        elif self.curr_stage == Stage.AUTOSEQUENCE:
            # nv1_actuation = self.registry.get(("valve_actuation", "actuation_type", ValveType.SOLENOID, ValveLocation.PRESSURIZATION))[1]
            # if nv1_actuation != ActuationType.CLOSE_VENT:
            #     self.flag.put(("solenoid", "actuation_type", ValveLocation.PRESSURIZATION), ActuationType.CLOSE_VENT)
            #     self.flag.put(("solenoid", "actuation_priority", ValveLocation.PRESSURIZATION), ValvePriority.PI_PRIORITY)
            mpv_actuation = self.registry.get(("valve_actuation", "actuation_type", ValveType.SOLENOID, ValveLocation.MAIN_PROPELLANT_VALVE))[1]
            if curr - self.start_time > AUTOSEQUENCE_DELAY and mpv_actuation != ActuationType.OPEN_VENT:
                # Actuate valve
                self.flag.put(("solenoid", "actuation_type", ValveLocation.MAIN_PROPELLANT_VALVE), ActuationType.OPEN_VENT)
                self.flag.put(("solenoid", "actuation_priority", ValveLocation.MAIN_PROPELLANT_VALVE), ValvePriority.PI_PRIORITY)
        elif self.curr_stage == Stage.POSTBURN:
            #TODO: Make sure this actuation is correct
            if not self.actuated_postburn:
                # Actuate valves
                # self.flag.put(("solenoid", "actuation_type", ValveLocation.PRESSURIZATION), ActuationType.CLOSE_VENT)
                # self.flag.put(("solenoid", "actuation_priority", ValveLocation.PRESSURIZATION), ValvePriority.PI_PRIORITY)
                self.flag.put(("solenoid", "actuation_type", ValveLocation.PRESSURIZATION_VALVE), ActuationType.OPEN_VENT)
                self.flag.put(("solenoid", "actuation_priority", ValveLocation.PRESSURIZATION_VALVE), ValvePriority.PI_PRIORITY)
                self.flag.put(("solenoid", "actuation_type", ValveLocation.MAIN_PROPELLANT_VALVE), ActuationType.OPEN_VENT)
                self.flag.put(("solenoid", "actuation_priority", ValveLocation.MAIN_PROPELLANT_VALVE), ValvePriority.PI_PRIORITY)
                self.actuated_postburn = True
        else:
            raise Exception("Unknown stage: {}".format(str(self.curr_stage)))


    def execute(self):
        self.curr_stage = self.registry.get(("general", "stage"))[1] # This shouldn't affect anything
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
