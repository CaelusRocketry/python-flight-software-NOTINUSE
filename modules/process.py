import time, threading
from . import external
from . import telemetry

critical = {"temp": [-10232, 1001, f1, Value(False))], "pressure":[232, 323, f2, Value(False)] ... }
delay = 0.01

def start():
    iter = 0
    start_time = time.time()
    while True:
        # temp = time.time()
        # while time.time() - temp < delay: pass #replace line with time.sleep(delay) if you prefer
        while time.time() - (start_time + delay*iter) < 0: pass
        data = external.get_data()
        for category, number in data:
            if not critical[category][-1].value and (number < critial[category][0] or number > critial[category][1]):
                # do some correction in seperate thread, flag correction as done
                critical[category][-1].value = True
                t = threading.Thread(f=critical[category][-2], args=(number, critical[category][-1]))
                t.start()
                # when thread finishes thread will modify value
        telemetry.push(time.time() - start_time, data)
        iter += 1
