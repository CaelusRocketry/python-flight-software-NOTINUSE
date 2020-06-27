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
    //TODO: make sure that the pressure relief valve is the only thing that has to be actuated in this scenario
    for(string &loc : Util::parse_json_list({"sensors", "list", "pressure"})) {
        if(int(this->registry->get<SensorStatus>("sensor_status.pressure." + loc)) == int(SensorStatus::CRITICAL)) {
            Util::enqueue(this->flag, Log("response", "{\"header\": \"info\", \"Description\": \"Pressure in " + loc + " is too high; actuating pressure relief valve.\"}"), LogPriority::CRIT);
            this->flag->put("valve_actuation_type.solenoid.pressure_relief", ActuationType::OPEN_VENT);
            this->flag->put("valve_actuation_priority.solenoid.pressure_relief", ValvePriority::MAX_TELEMETRY_PRIORITY);
        }
    }
}