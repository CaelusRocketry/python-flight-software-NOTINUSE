from smbus2 import SMBus
from threading import Thread
import time
import socket
import heapq
from . import tvc
from main import load_config

messageQueue = []
BUFFER = 1024
config = load_config()

def createReceivingSocket(MY_IP, RECV_PORT):
    """
    Creates and connects a socket used for receiving.
    An error will occur  after some time if there is no response from the ground station.
    :param MY_IP: IP of the raspberry PI.
    :param RECV_PORT: Port meant to be used for receiving socket.
    """
    global sock_receive, conn_receive
    sock_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_receive.bind((MY_IP, RECV_PORT))
    sock_receive.listen(1)
    conn_receive, addr = sock_receive.accept()

def enqueue(message, timestamp, priority=1):
    """
    Enqueue a message to be sent.
    :param message: message to add to the message queue
    :param timestamp: time when message was conceived
    :param priority: priority status of message - default is 1, emergency is 0
    """
    heapq.heappush(messageQueue, (priority, message, timestamp))


def send():
    """
    Loops through the messages in the queue and sends them to ground using sockets.
    Delay of 50ms between each send.
    """
    global sock_send

    while True:
        if len(messageQueue) > 0:
            priority, message, timestamp = heapq.heappop(messageQueue)
            message = message.encode('utf-8')
            sock_send.sendall(message + '\r')
            print(message + "\t" + "Time: " + timestamp)
        time.sleep(50.0/1000.0)

def t_connect(groundstationIP, sendPort):
    """
    Creates and connects socket used for sending with the given IP and port.
    Assumes the ground station receiving socket is attempting to connect.
    :param groundstationIP: IP address of the ground station.
    :param sendPort: Port meant to be used for the sending socket.
    """
    global sock_send
    sock_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_send.connect((groundstationIP, sendPort))

def t_read():
    """
    Reads the next message from the ground or stalls until a message is available.
    BUFFER value can be changed by other methods.
    :return a: decoded string message that was received.
    """
    global conn_receive
    a = conn_receive.recv(BUFFER)
    a = a.decode('utf-8')
    return a

def listen():
    global sock_receive, conn_receive
    while 1:
        data = t_read()
        if data == "END CONNECTION":
            break
        messageDigest(data)

    conn_receive.close()
    sock_receive.close()

def messageDigest(message):
    """
    Reads message header and calls appropriate methods based on that.
    :param message:
    """
    if message == "CONNECT SENDING SOCKET":
        t_connect(config["modules"]["telemetry"]["groundstationIP"], config["modules"]["telemetry"]["sendPort"])
        # TODO: Configure Ground Station IP and Port in config
        enqueue('We are connected!')

def start():
    """
    Creates and starts a thread for the receiving socket.
    """
    # TODO: Configure PI IP and Port in config
    createReceivingSocket(config["modules"]["telemetry"]["piIP"], config["modules"]["telemetry"]["receivePort"])
    recv_thread = Thread(target=listen)
    recv_thread.start()
