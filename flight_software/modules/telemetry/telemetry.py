import socket
import threading
import time
import json
import heapq
from queue import PriorityQueue
from . import logging, encryption
from .logging import Packet, Log
from collections import deque

BYTE_SIZE = 8192

DELAY = .05
DELAY_LISTEN = .05
DELAY_SEND = .25

SEND_ALLOWED = True


class Telemetry:
    """ Telemetry Class handles all communication """


    def __init__(self, IP, PORT):
        """ Based on given IP and port, create and connect a socket """
        # self.queue_send = []
        self.queue_send = PriorityQueue()
        # self.queue_ingest = deque([])
        self.queue_ingest = PriorityQueue()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((IP, PORT))
        print("Connected socket")


    def begin(self):
        """ Starts the send and listen threads """
        send_thread = threading.Thread(target=self.send)
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.daemon = True
        send_thread.daemon = True
        send_thread.start()
        listen_thread.start()
        # self.enqueue(Packet(message=input("")))  # Used for testing purposes


    def end(self):
        """ Kills socket connection """
        self.sock.shutdown()
        self.sock.close()


    def send(self):
        """ Constantly sends next packet from queue to ground station """
        while True:
            if self.queue_send and SEND_ALLOWED:
                # encoded = heapq.heappop(self.queue_send)[1]
                encoded = self.queue_send.get()[1]
                self.sock.send(encoded)
            time.sleep(DELAY_SEND)


    def listen(self):
        """ Constantly listens for any from ground station """
        while True:
            data = self.sock.recv(BYTE_SIZE)
            # self.queue_ingest.append(data)
            self.queue_ingest.put((data.level, data))
            time.sleep(DELAY_LISTEN)


    def enqueue(self, packet):
        """ Encripts and enqueues the given Packet """
        packet_string = packet.to_string()  # Converts packet to string form
        print("Enqueueing", packet_string)
        encoded = encryption.encrypt(packet_string)
        # heapq.heappush(self.queue_send, (packet.level, encoded))
        self.queue_send.put((packet.level, encoded))
