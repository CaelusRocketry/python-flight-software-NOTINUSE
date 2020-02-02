import time
import json
from enum import IntEnum


class Level(IntEnum):
    """ Level Enum indicates the priority or status of the Packet """
    INFO = 4
    DEBUG = 3
    WARN = 2
    CRIT = 1


class Log:
    """ Packet class stores messages to be sent to and from ground and flight station """

    def __init__(self, header='heartbeat', message="alive", level: Level = Level.INFO,
                 timestamp: float = time.time(), sender="Flight Pi"):
        self.header = header
        self.message = message
        self.level = level
        self.timestamp = timestamp
        self.sender = sender
        f = open("black_box.txt", "a+")
        f.write("\n" + self.to_string())
        f.close()

    def to_string(self):
        ''' Convert Log dict to string for printing '''
        print(self.__dict__)
        return json.dumps(self.__dict__)

    def from_string(input_string):
        ''' Convert input_string to dictionary for Logging '''
        input_dict = json.loads(input_string)
        packet = Log()
        packet.__dict__ = input_dict
        return packet


class Packet:
    """ Packet class stores messages to be sent to and from ground and flight station """

    def __init__(self, header='heartbeat', logs: list = [], level: Level = Level.INFO, timestamp: float = time.time()):
        self.header = header
        self.logs = logs
        self.timestamp = timestamp
        self.level = level

    def add(self, log: Log):
        ''' Add log to list of logs '''
        self.logs.append(log)
        self.level = min(self.level, log.level)

    def to_string(self):
        ''' Turn all logs into strings from dictionary format '''
        output_dict = self.__dict__
        output_dict["logs"] = [log.to_string() for log in output_dict["logs"]]
        return json.dumps(self.__dict__)

    def from_string(input_string):
        ''' Turn all logs into dictionaries from strings '''
        input_dict = json.loads(input_string)
        print(input_dict)
        input_dict["logs"] = [Log.from_string(log_str) for log_str in input_dict["logs"]]
        packet = Packet()
        packet.__dict__ = input_dict
        return packet