# The only point of this class is to slow down the code while testing
from modules.mcl.flag import Flag
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

        start_time = self.registry.get(("general", "mcl_start_time"))[-1]
        if start_time:
            # if mcl is finished early, delay it so that it reaches the minimum run time

            # Full busy loop strat
            # while self.min_mcl_run_time + start_time - time.time() > 0:
            #     pass


            # Mixed strat
            diff = self.min_mcl_run_time + start_time - time.time()
            while diff > 0:
                time.sleep(diff / 2)
                diff = self.min_mcl_run_time + start_time - time.time()

 
            # Full time.sleep strat
#            current_time = time.time()
#            if current_time < start_time + self.min_mcl_run_time:
#               time.sleep(start_time + self.min_mcl_run_time - current_time)


            # print(time.time() - start_time)
        self.registry.put(("general", "mcl_start_time"), time.time())
