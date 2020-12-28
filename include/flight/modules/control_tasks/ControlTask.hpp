//
// Created by adiv413 on 4/24/2020.
//

#ifndef FLIGHT_CONTROLTASK_HPP
#define FLIGHT_CONTROLTASK_HPP

#include <vector>
#include <set>
#include <flight/modules/control_tasks/Control.hpp>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>
#include <memory>

using namespace std;

// Class which runs/manages all the ControlTasks

class ControlTask {
private:
    vector<unique_ptr<Control>> controls;

public:
    ControlTask(const set<string>& config);
    void begin();
    void control();
};
#endif //FLIGHT_CONTROLTASK_HPP
