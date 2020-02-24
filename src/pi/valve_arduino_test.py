from modules.tasks.valve_arduino_task import ValveArduinoTask
from modules.mcl.supervisor import Supervisor

valve_arduino = ValveArduinoTask()
supervisor = Supervisor([valve_arduino])
supervisor.run()