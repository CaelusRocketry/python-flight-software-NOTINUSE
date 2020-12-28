//
// Created by adiv413 on 4/24/2020.
//

#include <flight/modules/control_tasks/ValveControl.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <flight/modules/lib/Util.hpp>
#include <flight/modules/mcl/Config.hpp>
#include <chrono>
#include <string>

ValveControl::ValveControl() {
    this->send_interval = global_config.valves.send_interval;
    this->last_send_time = 0;
}

void ValveControl::begin() {
    global_flag.log_info("response",R"({"header": "info", "Description": "Valve Control started"})");
}

void ValveControl::execute() {
    check_abort();
    auto current_time = chrono::system_clock::now().time_since_epoch().count();

    if (last_send_time == 0 || current_time > last_send_time + send_interval) {
        send_valve_data();
        last_send_time = current_time;
    }
}

void ValveControl::send_valve_data() {
    stringstream message;
    message << "{";

    for (const auto& valve_type_ : global_registry.valves) {
        for (const auto& valve_location_ : valve_type_.second) {
            string location = valve_location_.first;
            RegistryValveInfo valve_info = valve_location_.second;
            auto state = valve_info.state;
            auto actuation_type = valve_info.actuation_type;
            message << '\"' << valve_type_.first << "." << valve_location_.first << "\": {";
            message << R"("state": ")" << solenoid_state_names.at(int(state)) << "\", ";
            message << R"("actuation_type": ")" << actuation_type_names.at(int(actuation_type));
            message << "\"}";
            message << ", ";
        }
    }

    string message_str = message.str();
    message_str[message_str.length() - 2] = '}';
    message_str.erase(message_str.length() - 1);

    Util::enqueue(global_flag, Log("valve_data", message.str()), LogPriority::INFO);

    last_send_time = chrono::system_clock::now().time_since_epoch().count();
}

void ValveControl::abort() {
    for (const auto& valve_ : valves) {
        RegistryValveInfo valve_info = global_registry.valves[valve_.first][valve_.second];

        auto actuation_type = valve_info.actuation_type;
        auto actuation_priority = valve_info.actuation_priority;

        if (actuation_type != ActuationType::OPEN_VENT || actuation_priority != ValvePriority::ABORT_PRIORITY) {
            FlagValveInfo &valve_flag = global_flag.valves[valve_.first][valve_.second];
            valve_flag.actuation_type = ActuationType::OPEN_VENT;
            valve_flag.actuation_priority = ValvePriority::ABORT_PRIORITY;
        }
    }
}

// Set the actuation type to NONE, with ABORT_PRIORITY priority
void ValveControl::undo_abort() {
    for (const auto& valve_ : valves) {
        RegistryValveInfo valve_info = global_registry.valves[valve_.first][valve_.second];

        if (valve_info.actuation_priority == ValvePriority::ABORT_PRIORITY) {
            FlagValveInfo &valve_flag = global_flag.valves[valve_.first][valve_.second];
            valve_flag.actuation_type = ActuationType::NONE;
            valve_flag.actuation_priority = ValvePriority::ABORT_PRIORITY;
        }
    }
}

void ValveControl::check_abort() {
    if (global_registry.general.hard_abort || global_registry.general.soft_abort) {
        abort();
    } else if (!global_registry.general.soft_abort) {
        undo_abort();
    }
}