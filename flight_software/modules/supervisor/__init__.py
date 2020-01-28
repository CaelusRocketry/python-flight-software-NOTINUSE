### Import the necessary classes
from . import Flag, Registry
from helpers import *
from mode import Mode
from ../telemetry import Telemetry
from status import Status
import threading

### Intialize everything
flag = Flag()
registry = Registry()
telemetry = Telemetry()
telemetry.begin()

### Read
### TODO: [priority] Create Status class

### TODO: Get the current data for all the sensors (via the arduino) and update the data in the registry
### TODO: Get commands from ground and propogate the telemetry queue with those commands
### TODO: Figure out what to do with the telemetry queue commands
### TODO: Make the values in control stuff that actually works
### TODO: Do actuate()

def read():
    thermocouple_data = get_thermocouple_data()
    registry.put("thermocouple_gas", thermocouple_data.get("thermocouple_gas"))
    registry.put("thermocouple_liquid", thermocouple_data.get("thermocouple_liquid"))

    pressure_data = get_pressure_data()
    registry.put("pressure_gas", pressure_data.get("pressure_gas"))
    registry.put("pressure_pre_main", pressure_data.get("pressure_pre_main"))
    registry.put("pressure_post_main", pressure_data.get("pressure_post_main"))
    registry.put("pressure_post_cv", pressure_data.get("pressure_post_cv"))

    load_cell_data = get_load_cell_data()
    registry.put("load_cell_h20", load_cell_data.get("load_cell_h20"))

    ball_valve_data = get_ball_valve_data()
    registry.put("ball_valve_pres", ball_valve_data.get("ball_valve_pres"))
    registry.put("ball_valve_main", ball_valve_data.get("ball_valve_main"))

    solenoid_data = get_solenoid_data()
    registry.put("solenoid_valve_drain", solenoid_data.get("solenoid_valve_drain"))
    registry.put("solenoid_valve_depres", solenoid_data.get("solenoid_valve_depres"))

    ### Get data from telemetry queue

    telemetry_queue_data = telemetry.queue_ingest.queue
    registry.put("telemetry_queue", telemetry_queue_data)


### Control

def control():

    ### Check the values in the registry and make sure they are acceptable

    if registry.get("thermocouple_gas") > 250:
        registry.put("mode", Mode.SOFT)
        registry.put("thermocouple_gas_status", Status.CRITICAL)

    if registry.get("thermocouple_liquid") > 250:
        registry.put("mode", Mode.SOFT)
        registry.put("thermocouple_liquid_status", Status.CRITICAL)

    if registry.get("pressure_gas") > 250:
        registry.put("mode", Mode.SOFT)
        registry.put("pressure_gas_status", Status.CRITICAL)

    if registry.get("pressure_pre_main") > 250:
        registry.put("mode", Mode.SOFT)
        registry.put("pressure_pre_main_status", Status.CRITICAL)

    if registry.get("pressure_post_main") > 250:
        registry.put("mode", Mode.SOFT)
        registry.put("pressure_post_main_status", Status.CRITICAL)
        
    if registry.get("pressure_post_cv") > 250:
        registry.put("mode", Mode.SOFT)
        registry.put("pressure_post_cv_status", Status.CRITICAL)


    if registry.get("load_cell_h20") > 250:
        registry.put("mode", Mode.SOFT)
        registry.put("load_cell_h20_status", Status.CRITICAL)

    if registry.get("ball_valve_pres") > 250:
        registry.put("mode", Mode.SOFT)
        registry.put("ball_valve_pres_status", Status.CRITICAL)

    if registry.get("ball_valve_main") > 250:
        registry.put("mode", Mode.SOFT)
        registry.put("ball_valve_main_status", Status.CRITICAL)

    if registry.get("solenoid_valve_drain") > 250:
        registry.put("mode", Mode.SOFT)
        registry.put("solenoid_valve_drain_status", Status.CRITICAL)


    if registry.get("solenoid_valve_depres") > 250:
        registry.put("mode", Mode.SOFT)
        registry.put("solenoid_valve_depres_status", Status.CRITICAL)

    pack = Packet()

    ### If we're in soft or hard abort mode, notify ground control

    if registry.get("mode") == Mode.SOFT:
        log = Log(header = 'MODE', message = 'SOFT', level = 5)
        pack.add(log)
    elif registry.get("mode") == Mode.HARD:
        log = Log(header = 'MODE', message = 'HARD', level = 5)
        pack.add(log)
    else:
        ### Figure out what to do with the telemetry commands: if i == something: do something

        for i in registry.get("telemetry_queue"):
            pass

    telemetry.enqueue(pack)

### Actuate

def actuate():
    pass


while True:
    read()
    control()
    actuate()