from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.lib.packet import *

class ValveControl():
    def __init__(self, registry: Registry, flag: Flag, sensors: 'list', valves: 'list'):
        self.registry = registry
        self.flag = flag
        self.sensors = sensors
        self.valves = valves

    def execute(self):
        print("HI")