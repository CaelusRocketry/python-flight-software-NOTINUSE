import time
import json
from enum import IntEnum

INITIAL_TIME = time.time()

class LogPriority(IntEnum):
    """ LogPriority Enum indicates the priority or status of the Packet """

    INFO = 4
    DEBUG = 3
    WARN = 2
    CRIT = 1

class Log:
    """ Log class stores messages to be sent to and from ground and flight station """

    def __init__(self, header, message={}, timestamp: float = None):
        self.header = header
        self.message = message
        self.timestamp = time.time() - INITIAL_TIME if timestamp is None else timestamp


    def save(self, filename="blackbox.txt"):
        f = open(filename, "a+")
        f.write(self.to_string() + "\n")
        print(self.to_string())
        print() 
        f.close()


    def to_json(self):
        return {
            "header": self.header,
            "message": self.message,
            "timestamp": self.timestamp,
        }


    def to_string(self):
        return json.dumps(self.to_json())


    @staticmethod
    def from_string(input_string):
        input_dict = json.loads(input_string)
        log = Log(
            header=input_dict["header"],
            message=input_dict["message"],
            timestamp=input_dict["timestamp"],
        )
        return log


class Packet:
    """ Packet class stores groups of messages, which are grouped by LogPriority. """

    def __init__(
        self,
        logs: list = [],
        priority: LogPriority = LogPriority.INFO,
        timestamp: float = None,
    ):
        self.logs = logs
        self.timestamp = time.time() - INITIAL_TIME if timestamp is None else timestamp
        self.priority = priority


    def add(self, log: Log):
        self.logs.append(log)


    def to_string(self):
        return json.dumps(
            {
                "logs": [log.to_json() for log in self.logs],
                "timestamp": self.timestamp,
                "priority": self.priority
            }
        )


    @staticmethod
    def from_string(input_string):
        input_dict = json.loads(input_string)

        return Packet(
            [
                Log(log["header"], log["message"], log["timestamp"])
                for log in input_dict["logs"]
            ],
            input_dict["priority"],
            input_dict["timestamp"],
        )


    def __lt__(self, other):
        if self.priority != other.priority:
           return self.priority - other.priority
        return other.timestamp - self.timestamp


    def __cmp__(self, other):
        if self.priority != other.priority:
            return self.priority - other.priority
        return other.timestamp - self.timestamp
