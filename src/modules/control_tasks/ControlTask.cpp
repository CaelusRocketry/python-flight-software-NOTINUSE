//
// Created by adiv413 on 4/24/2020.
//

#include <flight/modules/control_tasks/ControlTask.hpp>
#include <flight/modules/control_tasks/TelemetryControl.hpp>
#include <flight/modules/control_tasks/SensorControl.hpp>
#include <flight/modules/control_tasks/StageControl.hpp>
#include <flight/modules/control_tasks/ValveControl.hpp>
#include <flight/modules/control_tasks/PressureControl.hpp>


ControlTask::ControlTask(Registry *registry, Flag *flag, unordered_map<string, bool> config) {
    log("Control Task started");
    this->registry = registry;
    this->flag = flag;

    if(config.at("sensor")) {
        controls.push_back(unique_ptr<Control>(new SensorControl(registry, flag)));
    }
    if(config.at("telemetry")) {
        controls.push_back(unique_ptr<Control>(new TelemetryControl(registry, flag)));
    }
    if(config.at("valve")) {
        controls.push_back(unique_ptr<Control>(new ValveControl(registry, flag)));
    }
    if(config.at("stage")) {
        controls.push_back(unique_ptr<Control>(new StageControl(registry, flag)));
    }
    if(config.at("pressure")) {
        controls.push_back(unique_ptr<Control>(new PressureControl(registry, flag)));
    }
    Util::enqueue(this->flag, Log("response", "{\"header\": \"info\", \"Description\": \"Control Tasks started\"}"), LogPriority::INFO);
}

void ControlTask::begin() {
    for(auto &ctrl : this->controls) {
        ctrl.get()->begin();
    }
}

void ControlTask::control() {
    for(auto &ctrl : this->controls) {
        ctrl.get()->execute();
    }
}