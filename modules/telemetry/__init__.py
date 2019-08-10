import heapq
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast  
import socket, json, time, threading
import multiprocessing
import tcp_socket

queue_send=[]

def start():
    sock = tcp_socket.create_socket()
    send_thread = threading.Thread(target=tcp_socket.send, args=(sock,))
    listen_thread = threading.Thread(target=tcp_socket.listen, args=(sock,))
    send_thread.start()
    listen_thread.start()
    print("Listening and sending")

def encode(packet):
    with open("publickey.txt", "rb") as publickey:
        return RSA.importKey(publickey.read()).encrypt(packet)

def decode(message):
    with open("privatekey.txt", "rb") as privatekey:
        return RSA.importKey(privatekey.read()).decrypt(message)

def decode(message):
    with open("privatekey.txt", "rb") as privatekey:
        return RSA.importKey(privatekey.read()).decrypt(message)
