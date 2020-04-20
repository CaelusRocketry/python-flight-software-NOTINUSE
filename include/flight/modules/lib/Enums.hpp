//
// Created by adiv413 on 4/20/2020.
//

#ifndef FLIGHT_ENUMS_HPP
#define FLIGHT_ENUMS_HPP

//map enums to strings: https://stackoverflow.com/a/24296298/11043216

enum class SensorType {
    THERMOCOUPLE,
    PRESSURE,
    LOAD
};

enum class SensorLocation {
    CHAMBER,
    TANK,
    INJECTOR
};

enum class SolenoidState {
    OPEN,
    CLOSED
};

enum class SensorStatus {
    SAFE = 3,
    WARNING = 2,
    CRITICAL = 1
};

enum class ValveType {
    SOLENOID,
    BALL
};

enum class ValveLocation {
    PRESSURE_RELIEF,
    PROPELLANT_VENT,
    MAIN_PROPELLANT_VALVE
};

enum class ActuationType {
    PULSE,
    OPEN_VENT,
    CLOSE_VENT,
    NONE
};

enum class ValvePriority {
    NONE = 0,
    LOW_PRIORITY = 1,
    PI_PRIORITY = 2,
    MAX_TELEMETRY_PRIORITY = 3,
    ABORT_PRIORITY = 4
};

enum class Stage {
    PROPELLANT_LOADING,
    LEAK_TESTING_1,
    PRESSURANT_LOADING,
    LEAK_TESTING_2,
    PRE_IGNITION,
    DISCONNECTION
};

#endif //FLIGHT_ENUMS_HPP
