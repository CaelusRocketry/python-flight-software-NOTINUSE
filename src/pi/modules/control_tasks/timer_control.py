# The only point of this class is to slow down the code while testing
import time

class TimerControl:

    def __init__(self, registry, flag):
        pass

    def begin(self, config: dict):
        self.config = config
        self.delay = self.config["timer"]["delay"]

    def busy_wait(self, target):  
        current_time = time.time()
        while (time.time() <= current_time + target):
            pass
        print(time.time() - current_time)

    def execute(self):
        self.busy_wait(self.delay)
