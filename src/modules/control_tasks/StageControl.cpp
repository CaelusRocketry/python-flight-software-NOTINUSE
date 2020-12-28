#include <flight/modules/control_tasks/StageControl.hpp>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <Logger/logger_util.h>
#include <chrono>

StageControl::StageControl() {
    this->start_time = chrono::system_clock::now().time_since_epoch().count();
    this->send_interval = global_config.stages.send_interval;
    this->stage_index = 0;

    global_flag.log_info("response", {
        {"header", "info"},
        {"Description", "Stage Control started"}
    });
}


void StageControl::begin() {
    log("Stage control: Beginning");

    global_registry.general.stage = stage_names.at(stage_index);
    global_registry.general.stage_status = 0.0;
}

void StageControl::execute() {
    double status = calculate_status();
    global_registry.general.stage_status = status;
    bool &progress_flag = global_flag.general.progress;
    if (progress_flag) {
        this->progress();
        progress_flag = false;
    } else if (status >= 100) {
        send_progression_request();
    }

    stage_valve_control();
    send_data();
}

double StageControl::calculate_status() const {
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

void StageControl::send_progression_request() {
    global_flag.log_critical("response", {
        {"header", "stage_progression_request"},
        {"Description", "Request to progress to the next stage"}
    });
}

void StageControl::send_data() {
    if (this->send_time == 0 || chrono::system_clock::now().time_since_epoch().count() > (this->send_time + this->send_interval)) {
        global_flag.log_info("response", {
            {"header", "stage_data"},
            {"Stage", stage_strings.at(stage_index)},
            {"Status", to_string(calculate_status())}
        });
    }
}

void StageControl::progress() {
    double status = calculate_status();
    if (status != 100.0) {
        global_flag.log_critical("response", {
            {"header", "stage_progress"},
            {"Status", "Failure"},
            {"Description", "Stage progression failed, the rocket's not ready yet"}
        });
    } else {
        stage_index++;
        global_registry.general.stage = stage_names[stage_index];
        send_time = 0;
        global_registry.general.stage_status = calculate_status();
        start_time = chrono::system_clock::now().time_since_epoch().count();
        global_flag.log_critical("response", {
            {"header", "stage_progress"},
            {"Status", "Success"},
            {"Description", "Stage progression successful"}
        });
    }
}

void StageControl::stage_valve_control() {
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