//
// Created by adiv413 on 6/25/2020.
//

#include <flight/modules/control_tasks/PressureControl.hpp>
#include <flight/modules/lib/Util.hpp>


PressureControl::PressureControl(Registry *registry, Flag *flag) {
    this->registry = registry;
    this->flag = flag;
}

void PressureControl::begin() {
    Util::enqueue(this->flag, Log("response", "{\"header\": \"info\", \"Description\": \"Pressure Control started\"}"), LogPriority::INFO);
}

void PressureControl::execute() {
    check_pressure();
}

void PressureControl::check_pressure() {

    for(pair<string, string> matched : this->matchups) {
        if(int(this->registry->get<SensorStatus>("sensor_status.pressure." + matched.first)) == int(SensorStatus::WARNING)) { // why cast each to int?
            if(int(this->registry->get<SolenoidState>("valve.solenoid." + matched.second)) == int(SolenoidState::CLOSED)) {
                Util::enqueue(this->flag, Log("response", "{\"header\": \"info\", \"Description\": \"Pressure at " + matched.first + " is too high; opening " + matched.second + ".\"}"), LogPriority::CRIT);
                this->flag->put("valve_actuation_type.solenoid." + matched.second, ActuationType::OPEN_VENT);
                this->flag->put("valve_actuation_priority.solenoid." + matched.second, ValvePriority::MAX_TELEMETRY_PRIORITY);
            } 
        } else if(int(this->registry->get<SensorStatus>("sensor_status.pressure." + matched.first)) == int(SensorStatus::SAFE)) {
             if(int(this->registry->get<SolenoidState>("valve.solenoid." + matched.second)) == int(SolenoidState::OPEN)) {
                Util::enqueue(this->flag, Log("response", "{\"header\": \"info\", \"Description\": \"Pressure at " + matched.first + " is safe; closing " + matched.second + ".\"}"), LogPriority::CRIT);
                this->flag->put("valve_actuation_type.solenoid." + matched.second, ActuationType::CLOSE_VENT);
                this->flag->put("valve_actuation_priority.solenoid." + matched.second, ValvePriority::MAX_TELEMETRY_PRIORITY);
            } 
        }


    }


}