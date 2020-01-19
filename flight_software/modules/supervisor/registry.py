from mode import Mode

class Registry:

    self.values = {
        "thermocouple_gas": None,
        "thermocouple_liquid": None,
        "pressure_gas": None,
        "pressure_pre_main": None,
        "pressure_post_main": None,
        "pressure_post_cv": None,
        "load_cell_h20": None,
        "ball_valve_pres": None,
        "ball_valve_main": None,
        "solenoid_valve_drain": None,
        "solenoid_valve_depres": None,
        "telemetry_queue": [],
        "mode": None
    }

    self.types = {
        "thermocouple_gas": float,
        "thermocouple_liquid": float,
        "pressure_gas": float,
        "pressure_pre_main": float,
        "pressure_post_main": float,
        "pressure_post_cv": float,
        "load_cell_h20": float,
        "ball_valve_pres": int,
        "ball_valve_main": int,
        "solenoid_valve_drain": bool,
        "solenoid_valve_depres": bool,
        "telemetry_queue": list,
        "mode": Mode
    }

    def put(key, value, flag):
        if key not in self.values:
            flag.state_flags["state_put_error"] = True
            return False
        self.values[key] = value
        return True
        

    def get(key, flag):
        if key not in self.values:
            flag.state_flags["state_get_error"] = True
            return False
        return self.values[key]
