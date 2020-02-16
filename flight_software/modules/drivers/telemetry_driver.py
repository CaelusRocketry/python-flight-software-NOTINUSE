from modules.drivers.driver import Driver
from modules.mcl.logging import Packet
from enum import Enum
import socket
import threading
import heapq
import time

BUFFER = 8192

class Telemetry(Driver):
    
    """
    Initialize the Telemetry driver.
    Initialize the ingest queue, the send queue, the socket connection, and all other necessary variables.
    Also start all necessary threads
    """
    def __init__(self):
        # Set the socket's hardcoded values (ip address and port)
        self.GS_IP = '192.168.1.75'
        self.port = 5005
        self.DELAY_LISTEN = .05
        self.sock = None
        self.connection = False

        # Initialize the socket
        self.reset()
        self.recv_thread = threading.Thread(target=self.recv_loop, daemon=True)
        self.recv_thread.start()

    """
    The read method that is called during the Telmetry ReadTask.
    It should return everything in the ingest_queue.
    """
    def read(self) -> bytes:
        ret = [i for i in self.ingest_queue]
        self.ingest_queue = []
        return ret
        
    """
    The write method that is called during the Telemetry WriteTask.
    It should send everything in the send_queue over the socket connection.
    """
    def write(self, byte: bytes):
        for level, message in self.send_queue:
            self.socket.send(message)
        self.send_queue = []
        
    """
    This should be run in a thread, and should be constantly listening for data and appending to the ingest_queue.
    Should be called in __init__
    """
    def recv_loop(self):
        while True:
            data = self.sock.recv(BUFFER)
            heapq.heappush(self.ingest_queue, (data.level, data))
            time.sleep(self.DELAY_LISTEN)

    """
    This should add a given packet to the send_queue
    """
    def enqueue(self, packet: Packet):
        packet_string = packet.to_string()  
        heapq.heappush(self.send_queue, (packet.level, packet_string))

    def status(self) -> bool:
        return self.connection

    """
    Kills the connection and attempts to reconnect
    """
    def reset(self) -> bool:
        if self.sock is not None:
            self.end()
        self.connection = False
        
        self.ingest_queue = []
        self.send_queue = []

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("checkpoint #1")
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("checkpoint #2")
            self.sock.connect((self.GS_IP, self.port))
            print("checkpoint #3")
            self.connection = True
        except socket.error as error:
            print("Socket creation failed with error %s" %(error))               #what to do if it fails?
            self.connection = False

    """
    Kills socket connection 
    """
    def end(self):
        self.sock.shutdown()
        self.sock.close()
        self.connection = False