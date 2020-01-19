### Import Flag and Registry
from . import Flag, Registry
from helpers import *
from mode import Mode

### Intialize everything
flag = Flag()
registry = Registry()

### Read
### Get the current data for all the sensors (via the arduino) and update the data in the registry
### TODO: Get commands from ground and propogate the telemetry queue with those commands

def read():
    thermocouple_data = get_thermocouple_data()
    registry.put("thermocouple_gas", thermocouple_data.get("thermocouple_gas"))
    registry.put("thermocouple_liquid", thermocouple_data.get("thermocouple_liquid"))

    pressure_data = get_pressure_data()
    registry.put("pressure_gas", thermocouple_data.get("pressure_gas"))
    registry.put("pressure_pre_main", thermocouple_data.get("pressure_pre_main"))
    registry.put("pressure_post_main", thermocouple_data.get("pressure_post_main"))
    registry.put("pressure_post_cv", thermocouple_data.get("pressure_post_cv"))

    load_cell_data = get_load_cell_data()
    registry.put("load_cell_h20", thermocouple_data.get("load_cell_h20"))

    ball_valve_data() = get_ball_valve_data()
    registry.put("ball_valve_pres", thermocouple_data.get("ball_valve_pres"))
    registry.put("ball_valve_main", thermocouple_data.get("ball_valve_main"))

    solenoid_data = get_solenoid_data()
    registry.put("solenoid_valve_drain", thermocouple_data.get("solenoid_valve_drain"))
    registry.put("solenoid_valve_depres", thermocouple_data.get("solenoid_valve_depres"))

    telemetry_queue_data = get_telemetry_queue_data()
    registry.put("telemetry_queue", thermocouple_data.get("telemetry_queue"))



### Control

def control():
    # Measured in psi
    if registry.get("pressure_gas") > 250:
        flag.put("abort", Mode.ABORT)



### Actuate




