from modules.drivers.driver import Driver
from modules.lib.packet import Log, Packet
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
    def __init__(self, gs_ip: str, gs_port: int, delay: float):
        self.GS_IP = gs_ip
        self.GS_PORT = gs_port
        self.DELAY_LISTEN = delay
        self.DELAY_SEND = delay

        # Set the socket's hardcoded values (ip address and port)
        self.sock = None
        self.connection = False
        self.INGEST_LOCK = False
        self.recv_thread = None        
        self.ingest_queue = []
        self.send_queue = []


    """
    The read method that is called during the Telmetry ReadTask.
    It should return everything in the ingest_queue.
    """
    def read(self, num_messages: 'int') -> list:
        self.INGEST_LOCK = True
        all = False
        if num_messages > len(self.ingest_queue) or num_messages == -1:
            num_messages = len(self.ingest_queue)
            all = True
        ret = [heapq.heappop(self.ingest_queue) for i in range(num_messages)]
        if all:
            assert(len(self.ingest_queue) == 0)
        self.INGEST_LOCK = False
        return ret
        
    """
    The write method that is called during the Telemetry WriteTask.
    It should send everything in the send_queue over the socket connection.
    """
    def write(self, pack: Packet):
        pack_str = pack.to_string()
        pack_bytes = pack_str.encode()
        self.sock.send(pack_bytes)
        time.sleep(self.DELAY_SEND)
        
    """
    This should be run in a thread, and should be constantly listening for data and appending to the ingest_queue.
    Should be called in __init__
    """
    def recv_loop(self):
        while True:
            if self.connection:
                try:
                    data = self.sock.recv(BUFFER)
                except Exception as e:
                    print(str(e))
                    self.connection = False
                    return
                packet_str = data.decode()
                packet = Packet.from_string(packet_str)
                while self.INGEST_LOCK:
                    pass
                heapq.heappush(self.ingest_queue, packet)
                time.sleep(self.DELAY_LISTEN)
            else:
                return

    """
    Returns the status of the connection (True -> Connection alive, False -> Connection dead)
    """
    def status(self) -> bool:
        return self.connection

    """
    Kills the connection and attempts to reconnect
    """
    def reset(self) -> bool:
        self.recv_thread = None
        if self.sock is not None:
            self.end()
        
        self.ingest_queue = []
        self.send_queue = []
        try:
            self.connect()
        except socket.error as error:
            print("Socket creation failed with error %s" %(error))               #what to do if it fails?
            self.connection = False
            if self.sock is not None:
                self.end()

    """
    Creates the socket connection
    """
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((self.GS_IP, self.GS_PORT))
        self.connection = True
        self.INGEST_LOCK = False
        self.recv_thread = threading.Thread(target=self.recv_loop)
        self.recv_thread.start()
        self.connection = True


    """
    Kills socket connection 
    """
    def end(self):
        self.connection = False
        if self.sock is not None:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
            except Exception as e:
                print(str(e))
                print("Socket isn't connected, so shutdown failed")
        if self.recv_thread is not None:
            self.recv_thread.join()
        self.sock = None
        print("Successfully ended")
