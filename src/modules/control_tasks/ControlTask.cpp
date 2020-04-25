//
// Created by adiv413 on 4/24/2020.
//

#include <flight/modules/control_tasks/ControlTask.hpp>
#include <flight/modules/control_tasks/TelemetryControl.hpp>
#include <flight/modules/control_tasks/SensorControl.hpp>
#include <flight/modules/control_tasks/StageControl.hpp>
#include <flight/modules/control_tasks/ValveControl.hpp>


ControlTask::ControlTask(Registry *registry, Flag *flag, unordered_map<string, bool> config) {
    log("Control Task started");
    this->registry = registry;
    this->flag = flag;

    if(config.find("sensor") != config.end()) {
        controls.push_back(unique_ptr<Control>(new SensorControl(registry, flag)));
    }
    if(config.find("telemetry") != config.end()) {
        controls.push_back(unique_ptr<Control>(new TelemetryControl(registry, flag)));
    }
    if(config.find("valve") != config.end()) {
        controls.push_back(unique_ptr<Control>(new ValveControl(registry, flag)));
    }
    if(config.find("stage") != config.end()) {
        controls.push_back(unique_ptr<Control>(new StageControl(registry, flag)));
    }
}

void ControlTask::begin() {
    for(auto &ctrl : this->controls) {
        ctrl.get()->begin();
    }
    log("Control Tasks started"); //TODO: change this to enqueue
}

void ControlTask::control() {
    for(auto &ctrl : this->controls) {
        ctrl.get()->execute();
    }
}