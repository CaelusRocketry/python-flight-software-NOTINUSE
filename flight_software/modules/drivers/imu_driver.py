from modules.devices.device import Device
from enum import Enum

class IMU(Device):
    
    # Set the IMU's hardcoded interface values (ports)
    self.port = 0

    """
    Initialize the IMU driver
    """
    def __init__():
        pass

    """
    The read method that is called during the IMU ReadTask.
    This should read data from the IMU and return a dictionary of values.
    {linear_acceleration_x, linear_acceleration_y, linear_acceleration_z, pitch, yaw, roll}
    """
    def read(self) -> bytes:
        pass

    """
    The write method that is called during the IMU WriteTask.
    Probably the only time that we will use this is for calibration, but if you think of any other reasons to use this, jot them down.
    """
    def write(self, addr: hex, byte: bytes) -> None:
        pass

    def status(self) -> bool:
        pass

    def reset(self) -> bool:
        pass