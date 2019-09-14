import socket
import threading
import time
import json
import heapq
from . import packet, encryption
from .packet import Packet
from collections import deque

BYTE_SIZE = 8192

DELAY = .05
DELAY_LISTEN = .05
DELAY_SEND = .25

SEND_ALLOWED = True


class Telemetry:

    def __init__(self, IP, PORT):
        self.queue_send = []
        self.queue_ingest = deque([])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((IP, PORT))
        print("Connected socket")

    def begin(self):
        send_thread = threading.Thread(target=self.send)
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.daemon = True
        send_thread.daemon = True
        send_thread.start()
        listen_thread.start()
        # Used for testing purposes
#            self.enqueue(Packet(message=input("")))

    def end(self):
        self.sock.shutdown()
        self.sock.close()

    def send(self):
        while True:
            if self.queue_send and SEND_ALLOWED:
                encoded = heapq.heappop(self.queue_send)[1]
                self.sock.send(encoded)
            time.sleep(DELAY_SEND)

    def listen(self):
        while True:
            data = self.sock.recv(BYTE_SIZE)
            self.queue_ingest.append(data)
            time.sleep(DELAY_LISTEN)

    def enqueue(self, packet):
        packet_string = packet.to_string()
        print("Enqueueing", packet_string)
        encoded = encryption.encrypt(packet_string)
        heapq.heappush(self.queue_send, (packet.level, encoded))
