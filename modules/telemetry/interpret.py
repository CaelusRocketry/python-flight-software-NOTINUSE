import packet
import heapq
import socket
import tcp_socket
import subprocess
import types

ABORT = "ABORT"
TOK_DEL, TYPE_DEL = " ", ":"

def interpret(pck):
    print(pck)
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

    args = pck.message.split(TOK_DEL)[1:]
    args = list(map(lambda x: types[x.split(TYPE_DEL)[0]](x.split(TYPE_DEL)[1]), args))

    if pck.header in funcs:
        if pck.cmd in funcs[pck.header]:
            return str(funcs[pck.header][pck.cmd](*args))
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
