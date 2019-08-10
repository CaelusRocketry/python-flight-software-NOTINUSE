import heapq
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast  
import socket, json, time
import multiprocessing

queue_send=[]

def start():
    p = multiprocessing.Process(target=send_message)
    p.start()

def enqueue_packet(packet="Heartbeat", priority=1): #Encrypt then enqueue a message, if empyt send a heartbeat
    heapq.heappush(queue_send, (priority, packet))

def encode(packet):
    with open("publickey.txt", "rb") as privatekey:
        return RSA.importKey(privatekey.read()).encrypt(packet);

def send_messages():
    while True:
        try:
            heapq.heappop(queue_send)[1] #(priority, message)
        except IndexError:
            pass #Queue is empty
        
