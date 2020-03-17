from modules.lib.mode import Mode
from modules.lib.errors import AccessError
from modules.lib.enums import *

class Flag:

    def __init__(self):
        self.state_flags = {
            "abort": {
                "hard_abort": [],
                "soft_abort": []
            },
            "progress": {
                "stage": None
            },
            "sensor_request": {
                "thermocouple_chamber": None,
                "thermocouple_tank": None,
                "thermocouple_injector": None,
                "pressure_chamber": None,
                "pressure_tank": None,
                "pressure_injector": None,
                "load_chamber": None,
                "load_tank": None,
                "load_injector": None
            },
            "valve_request": {
                "ball_valve_pressure_relief": None,
                "ball_valve_propellant_vent": None,
                "ball_valve_main_propellant_valve": None,
                "solenoid_valve_pressure_relief": None,
                "solenoid_valve_propellant_vent": None,
                "solenoid_valve_main_propellant_valve": None
            },
            "telemetry": {
                "send_queue": [],
                "reset": True
            },
            "error": {
                "state_put_error": None,
                "state_get_error": None,
                "flag_put_error": None,
                "flag_get_error": None,
            },
            "valve": {
                "ball_valve_pres": None,
                "ball_valve_main": None,
                "solenoid_valve_drain": None,
                "solenoid_valve_depres": None,
            },
            "ball_valve_actuate": {
                "ball_valve_pressure_relief_pulse": None,
                "ball_valve_propellant_vent_pulse": None,
                "ball_valve_main_propellant_valve_pulse": None,
                "ball_valve_pressure_relief_open_vent": None,
                "ball_valve_propellant_vent_open_vent": None,
                "ball_valve_main_propellant_valve_open_vent": None,
                "ball_valve_pressure_relief_close_vent": None,
                "ball_valve_propellant_vent_close_vent": None,
                "ball_valve_main_propellant_valve_close_vent": None
            },
            "solenoid_valve_actuate": {
                "solenoid_valve_pressure_relief_pulse": None,
                "solenoid_valve_propellant_vent_pulse": None,
                "solenoid_valve_main_propellant_valve_pulse": None,
                "solenoid_valve_pressure_relief_open_vent": None,
                "solenoid_valve_propellant_vent_open_vent": None,
                "solenoid_valve_main_propellant_valve_open_vent": None,
                "solenoid_valve_pressure_relief_close_vent": None,
                "solenoid_valve_propellant_vent_close_vent": None,
                "solenoid_valve_main_propellant_valve_close_vent": None
            }
        }

        self.state_types = {
            "abort": {
                "hard_abort": list,
                "soft_abort": list
            },
            "progress": {
                "stage": Stage
            },
            "sensor_request": {
                "thermocouple_chamber": bool,
                "thermocouple_tank": bool,
                "thermocouple_injector": bool,
                "pressure_chamber": bool,
                "pressure_tank": bool,
                "pressure_injector": bool,
                "load_chamber": bool,
                "load_tank": bool,
                "load_injector": bool
            },
            "valve_request": {
                "ball_valve_pressure_relief": bool,
                "ball_valve_propellant_vent": bool,
                "ball_valve_main_propellant_valve": bool,
                "solenoid_valve_pressure_relief": bool,
                "solenoid_valve_propellant_vent": bool,
                "solenoid_valve_main_propellant_valve": bool
            },
            "telemetry": {
                "send_queue": list,
                "reset": bool
            },
            "error": {
                "state_put_error": bool,
                "state_get_error": bool,
                "flag_put_error": bool,
                "flag_get_error": bool,
            },
            "valve": {
                "ball_valve_pres": int,
                "ball_valve_main": int,
                "solenoid_valve_drain": bool,
                "solenoid_valve_depres": bool,
            },
            "ball_valve_actuate": {
                "ball_valve_pressure_relief_pulse": int,
                "ball_valve_propellant_vent_pulse": int,
                "ball_valve_main_propellant_valve_pulse": int,
                "ball_valve_pressure_relief_open_vent": int,
                "ball_valve_propellant_vent_open_vent": int,
                "ball_valve_main_propellant_valve_open_vent": int,
                "ball_valve_pressure_relief_close_vent": int,
                "ball_valve_propellant_vent_close_vent": int,
                "ball_valve_main_propellant_valve_close_vent": int
            },
            "solenoid_valve_actuate": {
                "solenoid_valve_pressure_relief_pulse": bool,
                "solenoid_valve_propellant_vent_pulse": bool,
                "solenoid_valve_main_propellant_valve_pulse": bool,
                "solenoid_valve_pressure_relief_open_vent": bool,
                "solenoid_valve_propellant_vent_open_vent": bool,
                "solenoid_valve_main_propellant_valve_open_vent": bool,
                "solenoid_valve_pressure_relief_close_vent": bool,
                "solenoid_valve_propellant_vent_close_vent": bool,
                "solenoid_valve_main_propellant_valve_close_vent": bool
            }
        }

    def put(self, key: 'tuple', value) -> AccessError:
        outer, inner = key
        if outer not in self.state_flags:
            print("OUTER ERROR")
            return AccessError.KEY_ERROR
        if inner not in self.state_flags[outer]:
            print("INNER ERROR", key)
            return AccessError.KEY_ERROR
        self.state_flags[outer][inner] = value
        return AccessError.NONE


    def get(self, key: 'tuple'):
        outer, inner = key
        if outer not in self.state_flags:
            return AccessError.KEY_ERROR
        if inner not in self.state_flags[outer]:
            return AccessError.KEY_ERROR
        return self.state_flags[outer][inner]