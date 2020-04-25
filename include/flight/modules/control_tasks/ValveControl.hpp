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

    void sendValveData();
    void abort();
    void undoAbort();
    void checkAbort();

public:
    ValveControl(Registry *registry, Flag *flag);
    void begin();
    void execute();
};

#endif //FLIGHT_VALVECONTROL_HPP
