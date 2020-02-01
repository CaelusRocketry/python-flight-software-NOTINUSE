from modules.devices.device import Device
from enum import Enum

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
        pass

    """
    The read method that is called during the Telmetry ReadTask.
    It should return everything in the ingest_queue.
    """
    def read(self) -> bytes:
        pass

    """
    The write method that is called during the Telemetry WriteTask.
    It should send everything in the send_queue over the socket connection.
    """
    def write(self, byte: bytes) -> None:
        pass

    """
    This should be run in a thread, and should be constantly listening for data and appending to the ingest_queue.
    Should be called in __init__
    """
    def recv_loop(self):
        pass

    """
    This should add a given packet to the send_queue
    """
    def enqueue(self, packet):
        pass

    def status(self) -> bool:
        pass

    def reset(self) -> bool:
        pass