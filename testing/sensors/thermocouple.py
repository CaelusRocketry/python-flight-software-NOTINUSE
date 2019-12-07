import sys
import os
sys.path.append("../../flight_software/modules/")
os.chdir("../../flight_software")
from sensors.thermocouple import Thermocouple

therm = Thermocouple(0, 0, "nose")

while True:
    print(therm.get_data())