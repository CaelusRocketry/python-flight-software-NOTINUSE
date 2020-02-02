from modules.devices.device import Device
from enum import Enum
import adafruit_bno055
import busio
import board

class IMU(Device):
    
    # Set the IMU's hardcoded interface values (ports)
    self.port = 0

    """
    Initialize the IMU driver
    """
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.imu = adafruit_bno055.BNO055(i2c)
        self.data = dict({"linear_acceleration_x", "linear_acceleration_y", "linear_acceleration_z", "pitch", "yaw", "roll"})
        self.mode = self.imu.mode

    """
    The read method that is called during the IMU ReadTask.
    This should read data from the IMU and return a dictionary of values.
    {linear_acceleration_x, linear_acceleration_y, linear_acceleration_z, pitch, yaw, roll}
    """
    def read(self) -> dict:
        self.data["linear_acceleration_x"] = self.imu.read_linear_acceleration()[0]
        self.data["linear_acceleration_y"] = self.imu.read_linear_acceleration()[1]
        self.data["linear_acceleration_z"] = self.imu.read_linear_acceleration()[2]

        self.data["yaw"] = self.imu.read_euler()[0]             # double check that this is the right method
        self.data["roll"] = self.imu.read_euler()[1]
        self.data["pitch"] = self.imu.read_euler()[2]

        return self.data

    """
    The write method that is called during the IMU WriteTask.
    Probably the only time that we will use this is for calibration, but if you think of any other reasons to use this, jot them down.
    """
    def write(self, addr: hex, byte: bytes) -> None:
        self.imu.mode(self.mode)

    def status(self) -> bool:
        return self.imu.calibrated()

    def reset(self) -> bool:
        self.imu._reset()
        return True