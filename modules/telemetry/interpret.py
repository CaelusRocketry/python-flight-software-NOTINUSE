import packet
import heapq
import socket
import tcp_socket
import subprocess

ABORT = "ABORT"
TOK_DEL, TYPE_DEL = " ", ":"

def interpret(pck):
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
        }
        # "sensor": {
        #     "temp": temp,
        #     "pressure": pressure,
        #     "gyro": gyro,
        # },
        # "valve": {
        #     "actuate": actuate_valve
        # }
    }

    tokens = pck.message.split(TOK_DEL)
    if len(tokens) == 1:
        return "ERROR: header found, missing command"
    else:
        header, cmd, args = *tokens[:2], tokens[2:]

    args = list(map(lambda x: types[x.split(TYPE_DEL)[0]](x.split(TYPE_DEL)[1]), args))

    if header in funcs:
        if cmd in funcs[header]:
            return str(funcs[header][cmd](*args))
        return "Unknown command!"
    return "Unknown header!"

def get_ip():
    return(subprocess.getoutput("hostname -I").split()[1])

def get_core_temp():
    #return(subprocess.getoutput("/opt/vc/bin/vcgencmd measure_temp"))
    return("48.0 C")

def get_core_speed():
    #return(subprocess.getoutput("lscpu | grep MHz").split()[1]+" MHz")
    return("1.400 MHz")

def abort():
    return("ABORTING")
