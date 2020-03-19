from modules.mcl.registry import Registry
from modules.mcl.flag import Flag
from modules.lib.packet import *

class SensorControl():
    def __init__(self):
        pass

    def execute(self, state_field_registry: Registry, flags: Flag):
        input_str = (
        "{" + 
            "thermocouple: {" + 
                "chamber: " + str(state_field_registry.get(("sensor", "thermocouple_chamber"))) + "," +
	            "tank: " + str(state_field_registry.get(("sensor", "thermocouple_tank"))) + "," +
	        "}," + 
            "pressure: {" + 
                "chamber: " + str(state_field_registry.get(("sensor", "pressure_chamber"))) + "," +
                "tank: " + str(state_field_registry.get(("sensor", "pressure_tank"))) + "," +
                "injector: " + str(state_field_registry.get(("sensor", "pressure_injector"))) + "," +
            "}," + 
            "load: {" + 
	            "tank: " + str(state_field_registry.get(("sensor", "load_tank"))) + "," +
            "}" + 
        "}"
        )

        packet = Packet.from_string(input_str)
        flags.get(("telemetry", "send_queue")).append(packet)

        #TODO: Make these values correspond with the sensors, right now they're just random

        if state_field_registry.get(("sensor", "thermocouple_chamber")) > 250:
            pass

        if state_field_registry.get(("sensor", "thermocouple_tank")) > 250:
            pass

        if state_field_registry.get(("sensor", "pressure_chamber")) > 250:
            pass

        if state_field_registry.get(("sensor", "pressure_tank")) > 250:
            pass

        if state_field_registry.get(("sensor", "pressure_injector")) > 250:
            pass
