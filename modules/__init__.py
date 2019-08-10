
import heapq
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast

queue_send=[]

def enqueue_packet(packet="Heartbeat", priority=1): #e
    heapq.heappush(queue_send, (priority, packet))

def encode(packet):
    