from types import *
import time, os, threading
import pandas as pd

class Sensor:

    def __init__(self, name: str,  location: int, normal: float, warn: float, crit: float, get_data: FunctionType, correct: FunctionType) -> None:
        self.name = name
        self.location = location
        self.normal = normal
        self.warn = warn
        self.crit = crit
        self.get_data = lambda: get_data(location)
        self.correct = lambda reading: correct(self, location, reading)
        self.corrected = False

locations = {}

def correct(sensor, location, reading):
    sensor.corrected = True
    print(f"Correction at {location} with reading {reading}")
    t = threading.Thread(target=subcorrect, args=(sensor, location,))
    t.start()

def subcorrect(sensor, location):
    time.sleep(3)
    print(f"Thread {location} ended")
    sensor.corrected = False

def get_temp(location):
    fname = f"{os.getcwd()}/modules/temp{location}.csv"
    if fname in locations:
        locations[fname] += 1
    else:
        locations[fname] = 0
    data = pd.read_csv(open(fname), squeeze=True)
    return data[locations[fname]]

def get_pressure():
    pass


def get_attitude():
    pass


def get_flow_rate():
    pass

sensors = [Sensor("temp", 1, 10, 20, 30, get_temp, correct), Sensor("temp", 2, 100, 200, 300, get_temp, correct)]
