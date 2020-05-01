//
// Created by Srikar on 4/15/2020.
//

#ifndef FLIGHT_VALVECONTROL_HPP
#define FLIGHT_VALVECONTROL_HPP

#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>
#include <vector>
#include <string>
#include <flight/modules/control_tasks/Control.hpp>

class ValveControl : public Control {
private:
    Registry *registry;
    Flag *flag;
    std::vector<std::string> valves;
    double send_interval;
    double last_send_time;

    vector<string> build_valves();
    const vector<string> actuation_type_names = {"NONE", "CLOSE_VENT", "OPEN_VENT", "PULSE"};
    const vector<string> solenoid_state_names = {"OPEN", "CLOSED"};
    const vector<string> valve_priority_names = {"NONE", "LOW_PRIORITY", "PI_PRIORITY", "MAX_TELEMETRY_PRIORITY", "ABORT_PRIORITY"};


    void send_valve_data();
    void abort();
    void undo_abort();
    void check_abort();

public:
    ValveControl(Registry *registry, Flag *flag);
    void begin();
    void execute();
};

#endif //FLIGHT_VALVECONTROL_HPP
