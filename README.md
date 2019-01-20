# Flight Software 
Flight software for Project Caelus, written in Python.


## Setup
Use **Pipenv** as the virtual environment. 
The *Pipfile* and *Pipfile.lock* are included in this repository.
More information on using Pipenv is available at https://pipenv.readthedocs.io/en/latest/.

This flight software is written in **Python 3.7**.


## Usage
Run `python3 main.py`. 
Ensure that `python3` points to the virtual environment's Python executable.


## Libraries
- `PyYAML`: Used to parse the configuration file, which is a *.yaml* file.


## Structure
- *main.py*
    - The file that is run
    - Use `python3 main.py`
    - Loops through submodules defined in *config.yml*
    - Starts the submodules
- *config.yml*
    - Configuration on what to run
    - Contains submodule-level parameters
- *modules/*
    - Each submodule has a `start()` function
    - *telemetry.py*
        - `enqueue()`
        - `send()`
        - `receive()`
    - *external.py*
        - Get methods for all sensors
        - Set methods for RCS and EDF (motors)
    - *tvc.py*
        - Calls get methods in *external.py*
        - Processing of sensor data and responding accordingly
        
