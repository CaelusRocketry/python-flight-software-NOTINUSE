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
        self.GS_IP = None
        self.GS_PORT = None
        self.DELAY_LISTEN = None
        self.sock = None
        self.connection = False

    """
    The read method that is called during the Telmetry ReadTask.
    It should return everything in the ingest_queue.
    """
    def read(self, num_messages) -> list:
        all = False
        if num_messages > len(self.ingest_queue) or num_messages == -1:
            num_messages = len(self.ingest_queue)
            all = True
        ret = [heapq.heappop(self.ingest_queue)[1] for i in range(num_messages)]
        if all:
            assert(len(self.ingest_queue) == 0)
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
            if self.connection:
                data = self.sock.recv(BUFFER)
                packet_str = data.decode()
                packet = Packet.from_string(packet_str)
                heapq.heappush(self.ingest_queue, (packet.level, packet))
                time.sleep(self.DELAY_LISTEN)
            else:
                return

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
    def reset(self, gs_ip, gs_port, delay_listen) -> bool:
        self.GS_IP = gs_ip
        self.GS_PORT = gs_port
        self.DELAY_LISTEN = delay_listen
        if self.sock is not None:
            self.end()
        
        self.ingest_queue = []
        self.send_queue = []

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.connect((self.GS_IP, self.GS_PORT))
            self.connection = True
            self.recv_thread = threading.Thread(target=self.recv_loop)
            self.recv_thread.start()
        except socket.error as error:
            print("Socket creation failed with error %s" %(error))               #what to do if it fails?
            self.connection = False
            if self.sock is not None:
                self.end()

    """
    Kills socket connection 
    """
    def end(self):
        self.connection = False
        if self.sock is not None:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        if self.recv_thread is not None:
            self.recv_thread.join()
