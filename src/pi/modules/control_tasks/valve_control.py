from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.lib.packet import *

class ValveControl():
    def __init__(self):
        pass

    def execute(self, state_field_registry: Registry, flags: Flag):
        print("HI")