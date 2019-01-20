from smbus2 import SMBus
from threading import Thread
import heapq

from . import tvc

messageQueue = []

def enqueue(message, priority=1):
    """
    Enqueue a message to be sent.
    :param message: Message to send.
    """

    global messageQueue

    heapq.heappush(messageQueue, (priority, message))


def send():
    """

    :return:
    """

    while True:
        while len(messageQueue) > 0:
            priority, message = heapq.heappop(messageQueue)
            # TODO: Actually send the message
            print(message)


def listen():
    pass


def start():
    pass
