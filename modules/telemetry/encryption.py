import heapq
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast  
import socket, json, time, threading
import multiprocessing
import tcp_socket
from Crypto.Cipher import PKCS1_OAEP
import zlib

queue_send=[]

def start():
    queue_send=[]
    sock = tcp_socket.create_socket()
    send_thread = threading.Thread(target=tcp_socket.send, args=(sock,))
    listen_thread = threading.Thread(target=tcp_socket.listen, args=(sock,))
    send_thread.start()
    listen_thread.start()
    print("Listening and sending")

def encode(packet):
    with open("public.pem", "rb") as publickey:
        key = RSA.import_key(publickey.read())
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(str.encode(packet))

def decode(message):
    with open("private.pem", "rb") as privatekey:
        key = RSA.import_key(privatekey.read())
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(ast.literal_eval(str(message))).decode("utf-8")
