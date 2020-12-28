//
// Created by adiv413 on 6/25/2020.
//

#include <flight/modules/control_tasks/PressureControl.hpp>
#include <flight/modules/lib/Util.hpp>

void PressureControl::begin() {
    Util::enqueue(global_flag, Log("response", "{\"header\": \"info\", \"Description\": \"Pressure Control started\"}"), LogPriority::INFO);
}

void PressureControl::execute() {
    check_pressure();
}

void PressureControl::check_pressure() {
    for(pair<string, string> matched : this->matchups) {
        auto registry_sensor = global_registry.sensors["pressure"][matched.first];
        auto registry_valve = global_registry.valves["solenoid"][matched.second];
        if (registry_sensor.status == SensorStatus::WARNING) {
            if (registry_valve.state == SolenoidState::CLOSED) {
                string log_string = "{\"header\": \"info\", \"Description\": \"Pressure at " + matched.first + " is too high; opening " + matched.second + ".\"}";
                Util::enqueue(global_flag, Log("response", log_string), LogPriority::CRIT);
                auto &valve_flag = global_flag.valves["solenoid"][matched.second];
                valve_flag.actuation_type = ActuationType::OPEN_VENT;
                valve_flag.actuation_priority = ValvePriority::MAX_TELEMETRY_PRIORITY;
            } 
        } else if (registry_sensor.status == SensorStatus::SAFE) {
            if (registry_valve.state == SolenoidState::OPEN) {
                string log_string = "{\"header\": \"info\", \"Description\": \"Pressure at " + matched.first + " is safe; closing " + matched.second + ".\"}";
                Util::enqueue(global_flag, Log("response", log_string), LogPriority::CRIT);
                auto &valve_flag = global_flag.valves["solenoid"][matched.second];
                valve_flag.actuation_type = ActuationType::CLOSE_VENT;
                valve_flag.actuation_priority = ValvePriority::MAX_TELEMETRY_PRIORITY;
            } 
        }
    }
}