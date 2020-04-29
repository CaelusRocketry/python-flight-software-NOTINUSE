#ifndef FLIGHT_VALVETASK_HPP
#define FLIGHT_VALVETASK_HPP

#define NUM_VALVES 3

#include <vector>
#include <flight/modules/tasks/Task.hpp>
#include <flight/modules/drivers/Arduino.hpp>
#include <flight/modules/lib/Enums.hpp>

class ValveTask : public Task {
private:
    Arduino* valve;
    vector<tuple<string, string>> valve_list;
public:
    ValveTask(Registry* r, Flag* f)
            : Task(r, f) {}
    void initialize();
    void read();
    void actuate();
};


#endif //FLIGHT_VALVETASK_HPP
