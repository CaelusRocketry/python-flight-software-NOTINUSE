from modules.mcl.flag import Flag
from modules.lib.packet import Log, LogPriority


def enqueue(flag: Flag, log: Log, logpriority: LogPriority):
    _, queue = flag.get(("telemetry", "enqueue"))
    queue.append((log, LogPriority.CRIT))
    flag.put(("telemetry", "enqueue"), queue)
