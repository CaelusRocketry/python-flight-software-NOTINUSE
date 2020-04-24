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
    double request_time;
    double send_time;
    double start_time;

    double calculateStatus();

    void sendProgressionRequest();
    void sendData();
    void progress();
    void stageValveControl();

public:
    StageControl(Registry& registry, Flag& flag);
    void execute();
};

#endif //FLIGHT_STAGECONTROL_HPP
