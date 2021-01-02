import time
import json
from enum import IntEnum


class LogPriority(IntEnum):
    """ Level Enum indicates the priority or status of the Packet """
    INFO = 4
    DEBUG = 3
    WARN = 2
    CRIT = 1


class Log:
    """ Log class stores messages to be sent to and from ground and flight station """

    def __init__(self, header, message={},
                 timestamp: float = None, save: bool = True):
        self.header = header
        self.message = message
        if timestamp is None:
            timestamp = time.time()
        self.timestamp = timestamp
        if save:
            self.save()


    def save(self, filename = "black_box.txt"):
        f = open(filename, "a+")
        f.write(self.to_string() + "\n")
        f.close()


    def to_string(self):
        return json.dumps(self.__dict__)

    def copy(self):
        return Log(self.header, self.message.copy(), self.timestamp, save=False)

    @staticmethod
    def from_string(input_dict):
        log = Log(header=input_dict['header'], message=input_dict['message'], timestamp=input_dict['timestamp'])
        log.__dict__ = input_dict
        return log


class Packet:
    """ Packet class groups together logs of similar priority """

    def __init__(self, logs: list = [], level: LogPriority = LogPriority.INFO, timestamp: float = None):
        self.logs = logs
        if timestamp is None:
            timestamp = time.time()
        self.timestamp = timestamp
        self.level = level


    def add(self, log: Log):
        self.logs.append(log)


    def to_string(self):
        output_dict = self.__dict__.copy()
        output_dict["logs"] = [log.copy().to_string() for log in output_dict["logs"]] #TODO: fix error: the ' shows up when doing to_string 
        # because list of strings -> ['apple', 'banana'] instead of [apple, banana] which breaks stuff in gs
        # supposed to be [{log1}, {log2}, etc]
        return json.dumps(output_dict)


    @staticmethod
    def from_string(input_string):
        input_dict = json.loads(input_string)
        input_dict["logs"] = [Log.from_string(log_str) for log_str in input_dict["logs"]]
        packet = Packet()
        packet.__dict__ = input_dict
        return packet
    

    def __lt__(self, other):
        if self.level != other.level:
           return self.level - other.level
        return other.timestamp - self.timestamp


    def __cmp__(self, other):
        if self.level != other.level:
            return self.level - other.level
        return other.timestamp - self.timestamp
