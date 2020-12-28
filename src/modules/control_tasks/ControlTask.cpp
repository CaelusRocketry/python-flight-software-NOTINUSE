//
// Created by adiv413 on 4/24/2020.
//

#include <flight/modules/control_tasks/ControlTask.hpp>
#include <flight/modules/control_tasks/TelemetryControl.hpp>
#include <flight/modules/control_tasks/SensorControl.hpp>
#include <flight/modules/control_tasks/StageControl.hpp>
#include <flight/modules/control_tasks/ValveControl.hpp>
#include <flight/modules/control_tasks/PressureControl.hpp>

ControlTask::ControlTask(const set<string>& config) {
    log("Control task: Adding controls");

    if (config.count("sensor")) {
        controls.push_back(unique_ptr<Control>(new SensorControl()));
    }

    if (config.count("telemetry")) {
        controls.push_back(unique_ptr<Control>(new TelemetryControl()));
    }

    if (config.count("valve")) {
        controls.push_back(unique_ptr<Control>(new ValveControl()));
    }

    if (config.count("stage")) {
        controls.push_back(unique_ptr<Control>(new StageControl()));
    }

    if (config.count("pressure")) {
        controls.push_back(unique_ptr<Control>(new PressureControl()));
    }

    global_flag.log_info("response", {
        {"header", "info"},
        {"Description", "Control Tasks started"}
    });
}

void ControlTask::begin() {
    log("Control task: Beginning");

    for (auto &control : this->controls) {
        control->begin();
    }
}

void ControlTask::control() {
    log("Control task: Controlling");

    for (auto &control : this->controls) {
        control->execute();
    }
}