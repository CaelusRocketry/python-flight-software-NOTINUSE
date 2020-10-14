import json

config = json.loads(open("hardware_config.json").read())

if config["arduino_type"] == "psuedo":
    from modules.drivers.pseudo_arduino import Arduino
else:
    from modules.drivers.real_arduino import Arduino
