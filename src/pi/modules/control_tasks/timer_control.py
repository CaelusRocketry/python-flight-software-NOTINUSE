# The only point of this class is to slow down the code while testing
from modules.mcl.registry import Flag
from modules.mcl.registry import Registry
import time

class TimerControl:

    def __init__(self, registry: Registry, flag: Flag):
        self.registry = registry
        self.flag = flag

    def begin(self, config: dict):
        self.config = config
        self.min_mcl_run_time = self.config["timer"]["delay"]

    def execute(self):
        # all values, including min_mcl_run_time, are in seconds

        start_time = self.registry.get(("general", "mcl_start_time"))
        current_time = time.time()
        
        # if mcl is finished early, delay it so that it reaches the minimum run time

        if current_time < start_time + self.min_mcl_run_time:
            time.delay(start_time + self.min_mcl_run_time - current_time)
