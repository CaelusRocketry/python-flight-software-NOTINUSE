# Flight Software

[![Build Status](https://travis-ci.org/ProjectCaelus/flight-software.svg?branch=master)](https://travis-ci.org/ProjectCaelus/flight-software)

Flight software for Project Caelus.
This software is written in **Python**, version **3.7**.


## Setup

**Pipenv** is used as the dependency manager.
More information on Pipenv is available [in the docs](https://docs.pipenv.org/en/latest/).


## Structure
- */main.py*
    - The file that is run
- */modules/*
    - Each submodule has a `start()` function
    - */modules/sensors/*
        - Contains `struct`s and `trait`s that are used in sensors
        - Contains *imu.rs*, *pressure.rs*, and *temperature.rs*
    - */modules/supervisor/*
        - Polls sensors on a specified interval, gets logs, passes them to telemetry
    - */modules/telemetry/*
        - Sends data through websockets
        
## Encryption
 - Public key is used for encryption, secret privatekey is stored in the remote pi for decryption
