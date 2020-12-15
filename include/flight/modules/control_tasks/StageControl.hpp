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
    vector<Stage> stage_names {Stage::WAITING,
                               Stage::PRESSURIZATION,
                              Stage::AUTOSEQUENCE,
                              Stage::POSTBURN};
    vector<string> stage_strings = Util::parse_json_list({"stages", "list"});

    const double AUTOSEQUENCE_DELAY = 5.0;
    const double POSTBURN_DELAY = 10.0;

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
