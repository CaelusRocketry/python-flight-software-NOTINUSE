import time
import json
from enum import Enum
import jsonpickle

class Level(Enum):
    INFO = 4
    DEBUG = 3
    WARN = 2
    CRIT = 1

class Packet:

    def __init__(self, header = 'heartbeat' , message = "alive" , level: Level = Level.INFO, timestamp: float = time.time(), sender: str = "Flight Pi"):
        self.header = header
        self.message = message
        self.level = level
        self.timestamp = timestamp
        self.sender = sender

    def to_string(self):
        return jsonpickle.encode(self)

    def from_string(input_string):
        return jsonpickle.decode(input_string)
