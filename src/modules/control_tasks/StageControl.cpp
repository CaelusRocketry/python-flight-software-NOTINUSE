#include <flight/modules/control_tasks/StageControl.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <flight/modules/lib/Errors.hpp>
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

    Stage stage_index = this->registry->get<Stage>("general.stage");

    if(stage_index == Stage::WAITING) {
        return 100.0;
    } else if(stage_index == Stage::PRESSURIZATION) {
       double pressure = this->registry->get<double>("sensor_normalized.pressure.PT-2");
       return std::min(100.0, pressure/4.9);
    }
    else if(stage_index == Stage::AUTOSEQUENCE) {
        ActuationType mpv_actuation = this->registry->get<ActuationType>("valve_actuation_type.solenoid.main_propellant_valve");
        if(mpv_actuation == ActuationType::OPEN_VENT) {
            return 100.0;
        } else {
            return std::min(((chrono::system_clock::now().time_since_epoch().count() - this->start_time) / this->AUTOSEQUENCE_DELAY)*100, 99.0);
        }
    }
    else if(stage_index == Stage::POSTBURN) {
        double pressure = this->registry->get<double>("sensor_normalized.pressure.PT-2");
        double inv = (pressure - 20.0) / 5.0;           // Assuming that "depressurization" means 20psi
        double progress = std::min(100.0, 100.0 - inv);
        return std::max(0.0, progress); //  makes sure that progress isn't negative
    }
    
    throw INVALID_STAGE();
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