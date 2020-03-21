# Flight Software

Flight software for Project Caelus.
This software is written in **Python**, version **3.7**.


## Setup

All necessary libraries can be installed using the following command: 
```
pip3 install -r requirements.txt
```


## Structure
- */main.py*
    - The file that is run
- */modules/*
    - */modules/drivers/*
        - Contains low level code for each 
        - There are 3 drivers: [arduino](flight_software/modules/drivers/arduino.py), [imu](flight_software/modules/drivers/imu_driver.py), and [telemetry](flight_software/modules/drivers/telemetry_driver.py)
    - */modules/tasks/*
        - Contains read, control, and actuate methods for each item
        - There are 4 items: [imu](flight_software/modules/tasks/imu_task.py), [sensors](flight_software/modules/tasks/sensor_arduino_task.py), [telemetry](flight_software/modules/tasks/telemetry_task.py), and [valves](flight_software/modules/tasks/valve_arduino_task.py)
    - */modules/supervisor/*
        - Highest level code, directly run by */main.py*
        - Instiantiates each of the tasks
        - Contains `flags`, `registries`, `errors`, and `statuses`
        - Runs the MCL loop, which runs read, control, and actuate for each task
            - read() updates the `registry` with new readings, 
            - control() makes decisions based on the SFR, and sets `flags` while doing so
            - actuate() performs actions dictated by the `flags`
