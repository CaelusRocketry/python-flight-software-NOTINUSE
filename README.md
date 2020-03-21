# Flight Software

Flight software for Project Caelus.
This software is written in **Python**, version **3.7**.


## Setup

All necessary libraries can be installed using the following command: 
```
pip3 install -r requirements.txt
```


## Structure
- */requirements.txt*
    - Contains all the necessary python imports
- */src/*
    - */src/arduino/*
        - Contains low level code for reading sensors and actuating valves
    - */src/pi/*
        - Contains three unit testing files for each of the main components: 
            */src/pi/sensor_test.py* [sensors], */src/pi/telemetry_test.py* [telemetry], */src/pi/valve_test.py* [valves]
        - */src/pi/config.json*
            - Initial configuration for sensors, valves, and telemetry
        - */src/pi/modules*
            - */src/pi/modules/mcl/*
                - Highest level code, instiantiates each of the tasks
                - Contains `flags` and `registries`
                - Runs the MCL (Main Control Loop), which runs read, control, and actuate for each task
                    - `read()` updates the `registry` with new readings, 
                    - `control()` makes decisions based on the `registry`, and sets `flags` while doing so
                    - `actuate()`performs actions dictated by the `flags`
            - */src/pi/modules/tasks/*
                - Low level code, performs the `read` part of the MCL 
                - Contains `tasks` which directly communicate with the Arduino to `read()` from sensors and `actuate()` valves
            - */src/pi/modules/control_tasks/*
                - Medium level code, performs the `control` part of the MCL
                    - */src/pi/modules/control_tasks/control_task.py*: instantiates the necessary control tasks
                    - */src/pi/modules/control_tasks/telemetry_control.py* `ingests` all the messages in the telemetry send queue and sets the proper `flags` based on those messages
                    - */src/pi/modules/control_tasks/sensor_control.py* sends sensor data to the ground station and sets `flags` if the data is outside the boundaries specified in */src/pi/config.json*
                    - */src/pi/modules/control_tasks/valve_control.py* sends valve data to the ground station and sets `flags` if the valves have been open for too long
            - */src/pi/modules/drivers/*
                - Low level code, sets up the Arduino, sensors, valves, and telemetry
            - */src/pi/modules/lib/*
                - Contains utility files that are used throughout all the modules
                    -  */src/pi/modules/lib/packet.py*
                        - Contains `Packets` and `Logs`, which contain the information that is sent to and from ground station via `Telemetry`

                    
