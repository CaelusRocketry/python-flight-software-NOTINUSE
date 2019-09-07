import time
import json
from enum import IntEnum


class Level(IntEnum):
    INFO = 4
    DEBUG = 3
    WARN = 2
    CRIT = 1


class Packet:

    def __init__(self, header='heartbeat', message="alive", level: Level = Level.INFO,
                 timestamp: float = time.time(), sender="Flight Pi"):
        self.header = header
        self.message = message
        self.level = level
        self.timestamp = timestamp
        self.sender = sender

    def to_string(self):
        return json.dumps(self.__dict__)

    def from_string(input_string):
        input_dict = json.loads(input_string)
        packet = Packet()
        packet.__dict__ = input_dict
        return packet
