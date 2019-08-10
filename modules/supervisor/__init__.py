import RPistepper as stp
# Pins include the pins that the stepper motor are connected to, numbers below are samples
# Open is positive, close is negative
pins = [17, 27, 10, 9]

def start():
    print("[supervisor.start]")

# Opens vent and drains valves
def abort():
    with stp.Motor(pins) as M:
        for i in range(10):               
            M.move(20)
            M.release() # saves power when motor is not moving

# Opens the valve to a certain amount of steps, specified by the parameter
def open_valve(step):
    with stp.Motor(pins) as M:
        for i in range(10):               
            M.move(step)
            M.release() 

# Close valve to a certain amount of steps, inserted with the parameter
def close_valve(step):
    with stp.Motor(pins) as M:
        for i in range(10):               
            M.move(step*-1)
            M.release()

# Valve opens for a certain amount then closes
def tank_pulse():
    with stp.Motor(pins) as M:
        for i in range(3):             
            M.move(20)
            M.release()
        time.sleep(3)
        for i in range(3):
            M.move(-20)
            M.release()

# Checks if the valve is open or not, open is true, close is false, not sure how to do this
def valve_check():
    pass
