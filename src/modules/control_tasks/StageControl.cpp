#include <flight/modules/control_tasks/StageControl.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <chrono>

StageControl::StageControl() {
    this->request_interval = stod(Util::parse_json_value({"stages", "request_interval"}));
    this->start_time = chrono::system_clock::now().time_since_epoch().count();
    this->send_interval = stod(Util::parse_json_value({"stages", "send_interval"}));
    this->stage_index = 0;
    global_flag.enqueue(Log("response", "{\"header\": \"info\", \"Description\": \"Stage Control started\"}"), LogPriority::INFO);
}


void StageControl::begin() {
    global_registry.general.stage = stage_names.at(stage_index);
    global_registry.general.stage_status = 0.0;
}

void StageControl::execute() {
    double status = calculateStatus();
    global_registry.general.stage_status = status;
    bool progress = global_flag.general.progress;
    if (progress) {
        this->progress();
        global_flag.general.progress = false;
    } else if (status >= 100) {
        sendProgressionRequest();
    }

    stageValveControl();
    sendData();
}

double StageControl::calculateStatus() const {
    Stage current_stage = global_registry.general.stage;

    if (current_stage == Stage::WAITING) {
        return 100.0;
    } else if (current_stage == Stage::PRESSURIZATION) {
       double pressure = global_registry.sensors["pressure"]["PT-2"].normalized_value;
       return std::min(100.0, pressure/4.9);
    } else if (current_stage == Stage::AUTOSEQUENCE) {
        ActuationType mpv_actuation = global_registry.valves["solenoid"]["main_propellant_valve"].actuation_type;
        if (mpv_actuation == ActuationType::OPEN_VENT) {
            return 100.0;
        } else {
            return std::min(((chrono::system_clock::now().time_since_epoch().count() - this->start_time) / this->AUTOSEQUENCE_DELAY)*100, 99.0);
        }
    } else if(current_stage == Stage::POSTBURN) {
        double pressure = global_registry.sensors["pressure"]["PT-2"].normalized_value;
        double inv = (pressure - 20.0) / 5.0;           // Assuming that "depressurization" means 20psi
        double progress = std::min(100.0, 100.0 - inv);
        return std::max(0.0, progress); //  makes sure that progress isn't negative
    }
    
    throw INVALID_STAGE();
}

void StageControl::sendProgressionRequest() {
    global_flag.enqueue(Log("response", "{\"header\": \"stage_progression_request\", \"Description\": \"Request to progress to the next stage\"}"), LogPriority::CRIT);
}

void StageControl::sendData() {
    if (this->send_time == 0 || chrono::system_clock::now().time_since_epoch().count() > (this->send_time + this->send_interval)) {
        global_flag.enqueue(Log("response", "{\"header\": \"stage_data\", \"Stage\": " + stage_strings.at(stage_index) + ", \"Status\": \"" + to_string(calculateStatus()) + "\"}"), LogPriority::INFO);
    }
}

void StageControl::progress() {
    double status = calculateStatus();
    if (status != 100.0) {
        global_flag.enqueue(Log("response", "{\"header\": \"stage_progress\", \"Status\": \"Failure\", \"Description\": \"Stage progression failed, the rocket's not ready yet\"}"), LogPriority::CRIT);
    } else {
        stage_index++;
        global_registry.general.stage = stage_names[stage_index];
        send_time = 0;
        request_time = 0;
        global_registry.general.stage_status = calculateStatus();
        start_time = chrono::system_clock::now().time_since_epoch().count();
        global_flag.enqueue(Log("response", "{\"header\": \"stage_progress\", \"Status\": \"Success\", \"Description\": \"Stage progression successful\"}"), LogPriority::CRIT);
    }
}

void StageControl::stageValveControl() {
    //TODO: make this actuate valves based on the current stage
//    if(stage_index == int(Stage::WAITING)) {
//
//    }
//    else if(stage_index == int(Stage::PRESSURIZATION)) {
//
//    }
//    else if(stage_index == int(Stage::AUTOSEQUENCE)) {
//
//    }
//    else if(stage_index == int(Stage::POSTBURN)) {
//
//    }

}