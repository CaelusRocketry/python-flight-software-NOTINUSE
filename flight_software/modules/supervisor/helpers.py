### TODO: Update dicts to get data from arduino

### Gets data from arduino and stores it in a dict
def get_thermocouple_data():
    ### Get data from arduino
    return {"thermocouple_gas": 1.0,
            "thermocouple_liquid": 2.0}

def get_pressure_data():
    return {"pressure_gas": 1.0,
        "pressure_pre_main": 1.0,
        "pressure_post_main": 1.0,
        "pressure_post_cv": 1.0,}

def get_load_cell_data():
    return {"load_cell_h20": 1.0}

def get_ball_valve_data():
    return {"ball_valve_pres": 1,
        "ball_valve_main": 1}

def get_solenoid_data():
    return {"solenoid_valve_drain": True,
        "solenoid_valve_depres": True}

def get_telemetry_queue_data():
    return {"telemetry_queue": [1.0]}