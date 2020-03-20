import time
from modules.mcl.flag import Flag
from modules.lib.errors import Error
from modules.mcl.registry import Registry
from modules.lib.packet import Log, LogPriority

class ValveControl():
    def __init__(self, registry: Registry, flag: Flag):
        self.registry = registry
        self.flag = flag

    
    def begin(self, config: dict):
        self.config = config
        self.sensors = self.config["sensors"]["list"]
        self.valves = self.config["valves"]["list"]
        self.send_interval = self.config["valves"]["send_interval"]
        self.last_send_time = None


    def send_valve_data(self):
        message = {}
        for valve_type in self.valves:
            message[valve_type] = {}
            for valve_loc in self.valves[valve_type]:
                err, val, timestamp = self.registry.get(("valve", valve_type, valve_loc))
                assert(err == Error.NONE)
                message[valve_type][valve_loc] = val
        log = Log(header="valve_data", message=message)
        err, enqueue = self.flag.get(("telemetry", "enqueue"))
        assert(err == Error.NONE)
        enqueue.append((log, LogPriority.INFO))
        err = self.flag.put(("telemetry", "enqueue"), enqueue)
        assert(err == Error.NONE)


    def execute(self):
        if self.last_send_time is None or time.time() - self.last_send_time > self.send_interval:
            self.send_valve_data()
            self.last_send_time = time.time()
        
        #TODO: Valves can't be open for too long
