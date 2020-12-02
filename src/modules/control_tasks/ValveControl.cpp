//
// Created by adiv413 on 4/24/2020.
//

#include <flight/modules/control_tasks/ValveControl.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <flight/modules/lib/Util.hpp>
#include <boost/any.hpp>
#include <chrono>
#include <string>

ValveControl::ValveControl(Registry *registry, Flag *flag) {
    this->registry = registry;
    this->flag = flag;
    Util::enqueue(this->flag, Log("response", "{\"header\": \"info\", \"Description\": \"Valve Control started\"}"), LogPriority::INFO);
}

void ValveControl::begin() {
    this->valves = build_valves();
    this->send_interval = stod(Util::parse_json_value({"valves", "send_interval"}));
    this->last_send_time = 0;
}

void ValveControl::execute() {
    check_abort();
    // chrono::system_clock::now().time_since_epoch().count(): get current time as a double
    if(last_send_time == 0 || chrono::system_clock::now().time_since_epoch().count() - last_send_time > send_interval) {
        send_valve_data();
        last_send_time = chrono::system_clock::now().time_since_epoch().count();
    }
}

vector<string> ValveControl::build_valves() {
    vector<string> ret;
    for(string &i : Util::parse_json({"valves", "list"})) {
        for(string &j : Util::parse_json_list({"valves", "list", i})) {
            ret.push_back(i + "." + j);
        }
    }
    return ret;
}

void ValveControl::send_valve_data() {
    string message = "{";

    for(string &valve : valves) {
        SolenoidState state = registry->get<SolenoidState>("valve." + valve);
        ActuationType actuation = registry->get<ActuationType>("valve_actuation_type." + valve);

        message += "\"" + valve + "\": {";
        message += "\"state\": \"" + solenoid_state_names.at(int(state)) + "\", \"actuation_type\": \"" + actuation_type_names.at(int(actuation)) + "\"";
        message += "}, ";
    }

    Util::enqueue(this->flag, Log("valve_data", message), LogPriority::INFO);
}

void ValveControl::abort() {
    for(string &valve : valves) {
        ActuationType actuation_type = registry->get<ActuationType>("valve_actuation_type." + valve);
        ValvePriority actuation_priority = registry->get<ValvePriority>("valve_actuation_priority." + valve);

        if(actuation_type != ActuationType::OPEN_VENT || actuation_priority != ValvePriority::ABORT_PRIORITY) {
            flag->put("valve_actuation_type." + valve, ActuationType::OPEN_VENT);
            flag->put("valve_actuation_priority." + valve, ValvePriority::ABORT_PRIORITY);
        }
    }
}

void ValveControl::undo_abort() {
    for(string &valve : valves) {
        // ActuationType actuation_type = registry->get<ActuationType>("valve_actuation_type." + valve);
        ValvePriority actuation_priority = registry->get<ValvePriority>("valve_actuation_priority." + valve);

        if(actuation_priority == ValvePriority::ABORT_PRIORITY) {
            flag->put("valve_actuation_type." + valve, ActuationType::NONE);
            flag->put("valve_actuation_priority." + valve, ValvePriority::ABORT_PRIORITY);
        }
    }
}

void ValveControl::check_abort() {
    if(registry->get<bool>("general.hard_abort") || registry->get<bool>("general.soft_abort")) {
        abort();
    } else if(!registry->get<bool>("general.soft_abort")) {
        undo_abort();
    }
}