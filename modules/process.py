import time
from . import external
from . import telemetry

delay = 10**-2

def telemetrypush(time, data):
    print(f"[{time}]: {data}")

def start():
    iters = 0
    start_time = time.time()
    #while True:
    while iters < 10:
        #while time.time() - (start_time + delay*iters) < 0: pass
        time.sleep(delay)
        data = []
        for sensor in external.sensors:
            reading = sensor.get_data()
            data.append(reading)
            if not sensor.corrected and reading >= sensor.crit:
                # do some correction in seperate thread, flag correction as done
                sensor.correct(reading)
                # when thread finishes thread will modify value
        #telemetry.push(time.time() - start_time, data)
        telemetrypush(time.time() - start_time, data)
        iters += 1

#start()
