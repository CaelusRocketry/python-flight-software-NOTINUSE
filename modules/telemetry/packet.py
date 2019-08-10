import time
import json
from enum import Enum

class Level(Enum):
    INFO = 4
    DEBUG = 3
    WARN = 2
    CRIT = 1

    def to_string(level: int):
        return str(level)

    def from_str(level: str):
        return int(string)

class Packet:

    def __init__(self, header = "", message = "", level: Level = Level.INFO, timestamp: float = time.time(), sender: str = "Flight Pi"):
        self.header = header
        self.message = message
        self.level = level
        self.timestamp = timestamp
        self.sender = sender

    def to_str(self):
        dict = {}
        dict['HEADER'] =  self.header
        dict['MESSAGE'] = self.message
        dict['LEVEL'] = Level.to_str(self.level)
        dict['TIMESTAMP'] += str(self.timestamp)
        dict['SENDER'] += self.sender
        return dict

    def from_str(log_str: str):
        dict = json.loads(log_str)
        assert(len(dict) == 5)
        header = dict['HEADER']
        message = dict['MESSAGE']
        level = Level.from_str(dict['LEVEL'])
        timestamp = float(dict['TIMESTAMP'])
        sender = dict['SENDER']
        return Packet(header=header, message=message, level=level, timestamp=timestamp, sender=sender)