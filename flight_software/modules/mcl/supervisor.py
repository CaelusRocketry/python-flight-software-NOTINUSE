### Import the necessary classes
from modules.mcl.flag import Flag
from modules.mcl.registry import Registry

class Supervisor:

    def __init__(self, tasks):
        self.flag = Flag()
        self.registry = Registry()
        self.tasks = tasks
    
    def read(self):
        for task in self.tasks:
            self.registry = task.read(self.registry)

    def control(self):
        for task in self.tasks:
            self.registry, self.flag = task.control(self.registry, self.flag)

    def actuate(self):
        for task in self.tasks:
            self.task.actuate(self.registry, self.flag)
    
    def run(self):
        while True:
            self.read()
            self.control()
            self.actuate()

### Read
### TODO: [priority] Create Status class

### TODO: Get the current data for all the sensors (via the arduino) and update the data in the registry
### TODO: Get commands from ground and propogate the telemetry queue with those commands
### TODO: Figure out what to do with the telemetry queue commands
### TODO: Make the values in control stuff that actually works
### TODO: Do actuate()