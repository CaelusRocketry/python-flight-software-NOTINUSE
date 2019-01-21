from smbus2 import SMBus
from threading import Thread
import time
import socket
import heapq
from . import tvc
from main import load_config

messageQueue = []

config = load_config()


def enqueue(message, timestamp, priority=1):
    """
    Enqueue a message to be sent.
    :param message: message to add to the message queue
    :param timestamp: time when message was conceived
    :param priority: priority status of message - default is 1, emergency is 0
    """
    global messageQueue
    heapq.heappush(messageQueue, (priority, message, timestamp))


def send():
    """
    Loops through the messages in the queue and sends them to ground using sockets.
    """

    while True:
        while len(messageQueue) > 0:
            priority, message, timestamp = heapq.heappop(messageQueue)
            # TODO: Actually send the message using sockets
            print(message + "\t" + "Time: " + timestamp)


def t_connect(HostIp, Port):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HostIp, Port))
    return


def t_write(D):
    s.send(D + '\r')
    return


def t_read():
    a = ""
    while a == "":
        a = s.recv(1)
    return a


def t_close():
    s.close()
    return


def listen():
    if t_read() == "start tvc":
        tvc.stabilize()


def start():
    t_connect(config["modules"]["telemetry"]["hostIP"], config["modules"]["telemetry"]["port"])
    # TODO: Configure HostIP and Port in config
    t_write('We are connected!')
