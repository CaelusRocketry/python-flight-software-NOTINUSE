from modules.devices.device import Device
from enum import Enum
import socket
import threading

class Telemetry(Device):
    
    # Set the socket's hardcoded values (ip address and port)
    self.GS_IP = '127.0.0.1'
    self.port = 5005

    """
    Initialize the Telemetry driver.
    Initialize the ingest queue, the send queue, the socket connection, and all other necessary variables.
    Also start all necessary threads
    """
    def __init__():
        self.ingest_queue = []
        self.send_queue = []
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection = True
        except socket.error as error:
            print "Socket creation failed with error %s" %(err) # not sure what I am supposed to do if it fails
            self.connection = False
        self.thread = threading.Threading(target=recv_loop, daemon=True)
        self.thread.start()

    """
    The read method that is called during the Telmetry ReadTask.
    It should return everything in the ingest_queue.
    """
    def read(self) -> bytes:
        return (*self.ingest_queue, sep = ",")

    """
    The write method that is called during the Telemetry WriteTask.
    It should send everything in the send_queue over the socket connection.
    """
    def write(self, byte: bytes) -> None:
        self.socket.send(self.send_queue)
        self.connection = True

    """
    This should be run in a thread, and should be constantly listening for data and appending to the ingest_queue.
    Should be called in __init__
    """
    def recv_loop(self):
        while True:
            data = self.socket.recv()
            self.ingest_queue.append(data)

    """
    This should add a given packet to the send_queue
    """
    def enqueue(self, packet):
        self.send_queue.append(packet)

    def status(self) -> bool:
        return self.connection   

    def reset(self) -> bool:
        self.socket.close()
        self.ingest_queue = []
        self.send_queue = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.thread = threading.Threading(target=recv_loop, daemon=True)
        self.thread.start()
