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
    //TODO: make this actually do something
    if(int(this->registry->get<SensorStatus>("sensor_status.pressure.chamber")) == int(SensorStatus::CRITICAL)) {
        //actuate specific valves
    }
    if(int(this->registry->get<SensorStatus>("sensor_status.pressure.tank")) == int(SensorStatus::CRITICAL)) {
        //actuate specific valves
    }
    if(int(this->registry->get<SensorStatus>("sensor_status.pressure.injector")) == int(SensorStatus::CRITICAL)) {
        //actuate specific valves
    }
}