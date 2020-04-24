//
// Created by Srikar on 4/15/2020.
//

#ifndef FLIGHT_STAGECONTROL_HPP
#define FLIGHT_STAGECONTROL_HPP

#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>

class StageControl {
private:
    Registry registry;
    Flag flag;
    double m_requestTime;
    double m_sendTime;
    double m_startTime;

    double calculateStatus();

    void sendProgressionRequest();
    void sendData();
    void progress();
    void stageValveControl();

public:
    StageControl(Registry, Flag);
    void execute();
};

#endif //FLIGHT_STAGECONTROL_HPP
