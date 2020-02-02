from modules.devices.device import Device
from enum import Enum
import adafruit_bno055

class IMU(Device):
    
    # Set the IMU's hardcoded interface values (ports)
    self.port = 0

    """
    Initialize the IMU driver
    """
    def __init__():
        global sensor
        i2c = busio.I2C(board.SCL, board.SDA)
        sensor = adafruit_bno055.BNO055(i2c)
        self.dict = {}
        self.mode = sensor.mode

    """
    The read method that is called during the IMU ReadTask.
    This should read data from the IMU and return a dictionary of values.
    {linear_acceleration_x, linear_acceleration_y, linear_acceleration_z, pitch, yaw, roll}
    """
    def read(self) -> dict:
        self.dict = dict({sensor.linear_acceleration_x, sensor.linear_acceleration_y, sensor.linear_acceleration_z, sensor.pitch, sensor.roll, sensor.yaw})
        return self.dict
    """
    The write method that is called during the IMU WriteTask.
    Probably the only time that we will use this is for calibration, but if you think of any other reasons to use this, jot them down.
    """
    def write(self, addr: hex, byte: bytes) -> None:
        sensor.mode(self.mode)

    def status(self) -> bool:
        return sensor.calibrated()

    def reset(self) -> bool:
        sensor._reset()
        return True