import socket, threading, time, json
import heapq
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import multiprocessing
from packet import Packet
import encryption

GS_IP = '192.168.1.26'
GS_PORT = 5005
BYTE_SIZE = 1024

DELAY = .05
DELAY_LISTEN = .05
DELAY_SEND = .05

queue_send=[]

SEND_ALLOWED=True

def create_socket():
    queue_send=[]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((GS_IP, GS_PORT))
    return sock

def send(sock):
    while True:
        if queue_send and SEND_ALLOWED:
            encoded = heapq.heappop(queue_send)[1]
            sock.send(encoded)
        time.sleep(DELAY_SEND)

def listen(sock):
    while True:
        data = sock.recv(BYTE_SIZE)
        ingest_thread = threading.Thread(target=ingest, args=(data,))
        ingest_thread.start()
        time.sleep(DELAY_LISTEN)

def enqueue(packet = Packet()):
    packet_string = packet.to_string()
    encoded = encryption.encode(json.dumps(packet_string))
    heapq.heappush(queue_send, (packet.level, encoded))

def ingest(encoded):
    packet_str = encryption.decode(encoded)
    packet = Packet.from_string(Packet.from_string(packet_str))
    print(packet)
