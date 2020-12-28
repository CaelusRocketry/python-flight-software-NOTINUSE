//
// Created by adiv413 on 6/25/2020.
//

#include <Logger/logger_util.h>
#include <flight/modules/control_tasks/PressureControl.hpp>

void PressureControl::begin() {
    log("Pressure control: Beginning");

    global_flag.log_info("response", {
        {"header", "info"},
        {"Description", "Pressure Control started"}
    });
}

void PressureControl::execute() {
    check_pressure();
}

void PressureControl::check_pressure() {
    for(const pair<string, string>& matched : this->matchups) {
        auto registry_sensor = global_registry.sensors["pressure"][matched.first];
        auto registry_valve = global_registry.valves["solenoid"][matched.second];

        // Warning state
        if (registry_sensor.status == SensorStatus::WARNING) {
            // Open the valve
            if (registry_valve.state == SolenoidState::CLOSED) {
                global_flag.log_critical("response", {
                    {"header", "info"},
                    {"Description", "Pressure at " + matched.first + " is too high; opening " + matched.second + "."}
                });

                FlagValveInfo &valve_flag = global_flag.valves["solenoid"][matched.second];
                valve_flag.actuation_type = ActuationType::OPEN_VENT;
                valve_flag.actuation_priority = ValvePriority::MAX_TELEMETRY_PRIORITY;
            }
        } else if (registry_sensor.status == SensorStatus::SAFE) {
            if (registry_valve.state == SolenoidState::OPEN) {
                global_flag.log_critical("response", {
                        {"header", "info"},
                        {"Description", "Pressure at " + matched.first + " is safe; closing " + matched.second + "."}
                });

                FlagValveInfo &valve_flag = global_flag.valves["solenoid"][matched.second];
                valve_flag.actuation_type = ActuationType::CLOSE_VENT;
                valve_flag.actuation_priority = ValvePriority::MAX_TELEMETRY_PRIORITY;
            } 
        }
    }
}