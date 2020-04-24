//
// Created by Srikar on 4/15/2020.
//

#ifndef FLIGHT_VALVECONTROL_HPP
#define FLIGHT_VALVECONTROL_HPP

#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>
#include <vector>
#include <string>

class ValveControl {
private:
    Registry registry;
    Flag flag;
    std::vector<std::string> valves;
    double m_sendInterval;
    double m_lastSendTime;

    void sendValveData();
    void abort();
    void undoAbort();
    void checkAbort();

public:
    ValveControl(Registry, Flag);
    void execute();
};

#endif //FLIGHT_VALVECONTROL_HPP
