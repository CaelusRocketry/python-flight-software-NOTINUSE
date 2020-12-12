//
// Created by adiv413 on 4/24/2020.
//

#include <flight/modules/control_tasks/StageControl.hpp>
#include <chrono>

StageControl::StageControl(Registry *registry, Flag *flag) {
    this->registry = registry;
    this->flag = flag;
    this->request_interval = stod(Util::parse_json_value({"stages", "request_interval"}));
    this->start_time = chrono::system_clock::now().time_since_epoch().count();
    this->send_interval = stod(Util::parse_json_value({"stages", "send_interval"}));
    this->stage_index = 0;
    Util::enqueue(this->flag, Log("response", "{\"header\": \"info\", \"Description\": \"Stage Control started\"}"), LogPriority::INFO);
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

    if(stage_index == int(Stage::PRESSURIZATION)) {

    }
    else if(stage_index == int(Stage::AUTOSEQUENCE)) {

    }
    else if(stage_index == int(Stage::POSTBURN)) {

    }


    return min((chrono::system_clock::now().time_since_epoch().count() - start_time) * 5, 100.0);
}

void StageControl::sendProgressionRequest() {
    Util::enqueue(this->flag, Log("response", "{\"header\": \"stage_progression_request\", \"Description\": \"Request to progress to the next stage\"}"), LogPriority::CRIT);
}

void StageControl::sendData() {
    if(this->send_time == 0 || chrono::system_clock::now().time_since_epoch().count() > (this->send_time + this->send_interval)) {
        Util::enqueue(this->flag, Log("response", "{\"header\": \"stage_data\", \"Stage\": " + stage_strings.at(stage_index) + ", \"Status: \"" + to_string(calculateStatus()) + "}"), LogPriority::INFO);
    }
}

void StageControl::progress() {
    double status = calculateStatus();
    if(status != 100.0) {
        Util::enqueue(this->flag, Log("response", "{\"header\": \"stage_progress\", \"Status\": \"Failure\", \"Description\": \"Stage progression failed, the rocket's not ready yet\"}"), LogPriority::CRIT);
    }
    else {
        this->stage_index++;
        this->registry->put("general.stage", this->stage_names.at(this->stage_index));
        this->send_time = 0;
        this->request_time = 0;
        this->registry->put("general.stage_status", calculateStatus());
        this->start_time = chrono::system_clock::now().time_since_epoch().count();

        Util::enqueue(this->flag, Log("response", "{\"header\": \"stage_progress\", \"Status\": \"Success\", \"Description\": \"Stage progression successful\"}"), LogPriority::CRIT);
    }
}

void StageControl::stageValveControl() {
    //TODO: make this actuate valves based on the current stage

//    if(stage_index == int(Stage::PRESSURIZATION)) {
//
//    }
//    else if(stage_index == int(Stage::AUTOSEQUENCE)) {
//
//    }
//    else if(stage_index == int(Stage::POSTBURN)) {
//
//    }

}