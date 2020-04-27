//
// Created by adiv413 on 4/24/2020.
//

#include <flight/modules/control_tasks/StageControl.hpp>
#include <chrono>

StageControl::StageControl(Registry *registry, Flag *flag) {
    log("Stage Control started");
    this->registry = registry;
    this->flag = flag;
    this->request_interval = stod(Util::parse_json_value({"stages", "request_interval"}));
    this->start_time = chrono::system_clock::now().time_since_epoch().count();
    this->send_interval = stod(Util::parse_json_value({"stages", "send_interval"}));
    this->stage_index = 0;
}


void StageControl::begin() {
    this->registry->put("general.stage", stage_names.at(stage_index));
    this->registry->put("general.stage_status", 0.0);
}

void StageControl::execute() {
    double status = calculateStatus();
    this->registry->put("general.stage_status", status);
    bool progress = this->flag->get<bool>("general.progress");

    if(progress) {
        this->progress();
        this->flag->put("general.progress", false);
    }
    else if(status == 100) {
        sendProgressionRequest();
    }

    stageValveControl();
    sendData();
}

double StageControl::calculateStatus() {
    //TODO: implement actual calculations for this
    //this method is supposed to calculate how far along we are in the current stage, right now
    //all it does is return how much time is elapsed and progress is made purely off of time elapsed for now

    //maybe progress should be purely manual and based off of commands from ground station?

    if(stage_index == int(Stage::PROPELLANT_LOADING)) {

    }
    else if(stage_index == int(Stage::LEAK_TESTING_1)) {

    }
    else if(stage_index == int(Stage::PRESSURANT_LOADING)) {

    }
    else if(stage_index == int(Stage::LEAK_TESTING_2)) {

    }
    else if(stage_index == int(Stage::PRE_IGNITION)) {

    }
    else if(stage_index == int(Stage::DISCONNECTION)) {

    }

    return min((chrono::system_clock::now().time_since_epoch().count() - start_time) * 5, 100.0);
}

void StageControl::sendProgressionRequest() {
    log("[Approval needed from ground station] Request to progress to the next stage"); //TODO: change to enqueue once telemetry is done
}

void StageControl::sendData() {
    if(this->send_time == 0 || chrono::system_clock::now().time_since_epoch().count() > (this->send_time + this->send_interval)) {
        //TODO: convert to enqueue once telemetry is done
        log("Current stage: " + stage_strings.at(stage_index) + ", Current status: " + to_string(calculateStatus()));
    }
}

void StageControl::progress() {
    double status = calculateStatus();
    if(status != 100.0) {
        //TODO: convert to enqueue once telemetry is done
        log("Stage progression failed, the rocket's not ready yet.");
    }
    else {
        this->stage_index++;
        this->registry->put("general.stage", this->stage_names.at(this->stage_index));
        this->send_time = 0;
        this->request_time = 0;
        this->registry->put("general.stage_status", calculateStatus());
        this->start_time = chrono::system_clock::now().time_since_epoch().count();

        //TODO: change to enqueue once telemetry is done

        log("Stage progression successful.");
    }
}

void StageControl::stageValveControl() {
    //TODO: make this actuate valves based on the current stage

    if(stage_index == int(Stage::PROPELLANT_LOADING)) {

    }
    else if(stage_index == int(Stage::LEAK_TESTING_1)) {

    }
    else if(stage_index == int(Stage::PRESSURANT_LOADING)) {

    }
    else if(stage_index == int(Stage::LEAK_TESTING_2)) {

    }
    else if(stage_index == int(Stage::PRE_IGNITION)) {

    }
    else if(stage_index == int(Stage::DISCONNECTION)) {

    }
}