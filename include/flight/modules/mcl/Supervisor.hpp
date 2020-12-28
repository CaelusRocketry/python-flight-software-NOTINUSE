#ifndef FLIGHT_SUPERVISOR_HPP
#define FLIGHT_SUPERVISOR_HPP

#include <iostream>
#include <vector>
#include <flight/modules/tasks/Task.hpp>
#include <flight/modules/control_tasks/ControlTask.hpp>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>

using namespace std;

class Supervisor {
    private:
        vector<Task*> tasks;
        ControlTask *control_task;
        void parse_config();

    public:
        Supervisor() = default;
        ~Supervisor();
        void initialize();
        void read();
        void control();
        void actuate();
        void run();
};

#endif //FLIGHT_SUPERVISOR_HPP