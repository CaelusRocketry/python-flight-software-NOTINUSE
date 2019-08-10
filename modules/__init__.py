
import heapq
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast  
import socket, json, time

queue_send=[]

def enqueue_packet(packet="Heartbeat", priority=1): #e
    heapq.heappush(queue_send, (priority, packet))

def encode(packet):
    with open("publickey.txt", "rb") as privatekey:
        return RSA.importKey(privatekey.read()).encrypt(packet);

def send_messages():
    heapq.heappop(quque_send)[1]