#ifndef FLIGHT_SENSORARDUINO_HPP
#define FLIGHT_SENSORARDUINO_HPP

#include <flight/modules/tasks/Task.hpp>

using namespace std;

class SensorTask : public Task {
private:

public:
    SensorTask(Registry* r, Flag* f)
    : Task(r, f) {}
    void initialize();
    void read();
    void actuate();
};


#endif //FLIGHT_SENSORARDUINO_HPP
