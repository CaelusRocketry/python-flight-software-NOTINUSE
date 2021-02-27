import json

config = json.loads(open("hardware_config.json").read())

if config["arduino_type"] == "pseudo":
    from modules.drivers.pseudo_arduino import Arduino
    print("fake arduino")
else:
    from modules.drivers.real_arduino import Arduino
   print("real arduino")
