//
// Created by Srikar on 4/15/2020.
//

#ifndef FLIGHT_STAGECONTROL_HPP
#define FLIGHT_STAGECONTROL_HPP

#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>
#include <flight/modules/control_tasks/Control.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <flight/modules/lib/Util.hpp>
#include <vector>

class StageControl : public Control {
private:
    Registry *registry;
    Flag *flag;
    double request_time;
    double send_time;
    double start_time;
    double request_interval;
    double send_interval;
    int stage_index;
    vector<Stage> stage_names {Stage::PROPELLANT_LOADING,
                              Stage::LEAK_TESTING_1,
                              Stage::PRESSURANT_LOADING,
                              Stage::LEAK_TESTING_2,
                              Stage::PRE_IGNITION,
                              Stage::DISCONNECTION};
    vector<string> stage_strings = Util::parse_json_list({"stages", "list"});

    double calculateStatus();
    void sendProgressionRequest();
    void sendData();
    void progress();
    void stageValveControl();

public:
    StageControl(Registry *registry, Flag *flag);
    void begin();
    void execute();
};

#endif //FLIGHT_STAGECONTROL_HPP
