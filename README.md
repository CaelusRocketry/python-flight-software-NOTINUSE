# Flight Software

[![Build Status](https://travis-ci.org/ProjectCaelus/flight-software.svg?branch=master)](https://travis-ci.org/ProjectCaelus/flight-software)

Flight software for Project Caelus.
This software is written in **Rust** version **2018**.


## Setup

**Cargo** is used as the dependency manager.
More information on Cargo is available [in the docs](https://doc.rust-lang.org/stable/cargo/).


## Usage

Use `cargo run` to start the flight software.


## Libraries

- `bno055`: Functions to interface with the BNO055 IMU.


## Structure
- */main.rs*
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
        
