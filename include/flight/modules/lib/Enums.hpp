//
// Created by adiv413 on 4/20/2020.
//

#ifndef FLIGHT_ENUMS_HPP
#define FLIGHT_ENUMS_HPP


// Level Enum indicates the priority or status of the Packet
enum class LogPriority {
    INFO = 4,
    DEBUG = 3,
    WARN = 2,
    CRIT = 1
};


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
    OPEN = 0,
    CLOSED = 1
};

enum class SensorStatus {
    SAFE = 3,
    WARNING = 2,
    CRITICAL = 1
};

static unordered_map<SensorStatus, string> sensor_status_map {
        {SensorStatus::CRITICAL, "CRITICAL"},
        {SensorStatus::WARNING, "WARNING"},
        {SensorStatus::SAFE, "SAFE"}
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
    NONE = 0,
    CLOSE_VENT = 1,
    OPEN_VENT = 2,
    PULSE = 3,
};

static unordered_map<string, ActuationType> actuation_type_map {
        {"NONE", ActuationType::NONE},
        {"CLOSE_VENT", ActuationType::CLOSE_VENT},
        {"OPEN_VENT", ActuationType::OPEN_VENT},
        {"PULSE", ActuationType::PULSE}
};

enum class ValvePriority {
    NONE = 0,
    LOW_PRIORITY = 1,
    PI_PRIORITY = 2,
    MAX_TELEMETRY_PRIORITY = 3,
    ABORT_PRIORITY = 4
};

static unordered_map<string, ValvePriority> valve_priority_map {
        {"NONE", ValvePriority::NONE},
        {"LOW_PRIORITY", ValvePriority::LOW_PRIORITY},
        {"PI_PRIORITY", ValvePriority::PI_PRIORITY},
        {"MAX_TELEMETRY_PRIORITY", ValvePriority::MAX_TELEMETRY_PRIORITY},
        {"ABORT_PRIORITY", ValvePriority::ABORT_PRIORITY}
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
