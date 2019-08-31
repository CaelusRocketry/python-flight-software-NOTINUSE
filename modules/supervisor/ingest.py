from modules.telemetry.packet import Packet
from modules.telemetry.encryption import decode
import subprocess

ABORT = "ABORT"
TOK_DEL, TYPE_DEL = " ", ":"

def ingest(encoded):
    packet_str = decode(encoded)
    pck = Packet.from_string(packet_str)
    print("Incoming:", pck.message)
    if pck.message=="AT":
        return "Enqueue", Packet(header="HEARTBEAT", message="OK")

    types = {"int": int,
             "float": float,
             "str": str,
            }

    funcs = {
        ABORT: {
            ABORT: abort,
        },
        "internet": {
            "ip": get_ip
        },
        "sensor": {
        #    "temp": temp,
        #     "pressure": pressure,
        #     "gyro": gyro,
        },
        # "valve": {
        #     "actuate": actuate_valve
        # }
    }

    tokens = pck.message.split(TOK_DEL)
    if len(tokens) == 1:
        return "Error", "Header found, but missing command"
    else:
        header, cmd, args = *tokens[:2], tokens[2:]

    args = list(map(lambda x: types[x.split(TYPE_DEL)[0]](x.split(TYPE_DEL)[1]), args))

    if header in funcs:
        if cmd in funcs[header]:
            return "Enqueue", str(funcs[header][cmd](*args))
        return "Error", "Unknown command!"
    return "Error", "Unknown header!"

def get_ip():
    return(subprocess.getoutput("hostname -I").split()[1])

def get_core_temp():
    #return(subprocess.getoutput("/opt/vc/bin/vcgencmd measure_temp"))
    return packet.Packet(header="DATA", message="48.0 C")

def get_core_speed():
    #return(subprocess.getoutput("lscpu | grep MHz").split()[1]+" MHz")
    return packet.Packet(header="DATA", message="1.400 MHz")

def abort():
    return packet.Packet(header="DATA", message="ABORTING")
