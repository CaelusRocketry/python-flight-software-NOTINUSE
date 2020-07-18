# The only point of this class is to slow down the code while testing
import time

class SlowControl:

    def __init__(self, registry, flag):
        self.wait_time = 0.7

    def begin(self, config):
        pass

    def execute(self):
        print("Waiting")
        time.sleep(0.7)
