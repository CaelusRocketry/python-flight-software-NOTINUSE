//
// Created by adiv413 on 4/24/2020.
//

#include <vector>
#include <flight/modules/control_tasks/Control.hpp>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>
#include <memory>

using namespace std;

#ifndef FLIGHT_CONTROLTASK_HPP
#define FLIGHT_CONTROLTASK_HPP

class ControlTask {
private:
    vector<unique_ptr<Control>> controls;
    Registry *registry;
    Flag *flag;

public:
    ControlTask(Registry *registry, Flag *flag, unordered_map<string, bool> config);
    void begin();
    void control();
};
#endif //FLIGHT_CONTROLTASK_HPP
