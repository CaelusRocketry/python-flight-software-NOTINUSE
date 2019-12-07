"""
Scripted program that initiates and briefly tests all hardware
 - get initial sensor readings
 - ground-flight connection verification
 - actuate all valves to full extent for one cycle

Once all systems are ready, need everyone to confirm on GUI that everything is ready.
Once that is confirmed, the flight director starts prestage script, basically just opening valves slowly. Then begin main program.
"""
from modules.telemetry import Telemetry


# get initial sensor readings

# ground-flight connection verification
GS_IP = '192.168.1.29'
GS_PORT = 5005
telem = Telemetry(GS_IP, GS_PORT)

print("Telemetry Connected")
