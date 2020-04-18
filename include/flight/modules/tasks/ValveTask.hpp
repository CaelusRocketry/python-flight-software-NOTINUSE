#ifndef FLIGHT_VALVETASK_HPP
#define FLIGHT_VALVETASK_HPP

#include <flight/modules/tasks/Task.hpp>

using namespace std;

class ValveTask : public Task {
private:

public:
    ValveTask(Registry* r, Flag* f)
            : Task(r, f) {}
    void initialize();
    void read();
    void actuate();
};


#endif //FLIGHT_VALVETASK_HPP
