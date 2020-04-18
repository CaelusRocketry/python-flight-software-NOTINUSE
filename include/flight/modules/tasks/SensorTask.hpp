#ifndef FLIGHT_SENSORARDUINO_HPP
#define FLIGHT_SENSORARDUINO_HPP

#define NUM_SENSORS 6

#include <vector>
#include <tuple>
#include <flight/modules/drivers/Arduino.hpp>
#include <flight/modules/tasks/Task.hpp>

class SensorTask : public Task {
private:
    Arduino* sensor;
    vector<tuple<string, string>> sensor_list;
public:
    SensorTask(Registry* r, Flag* f)
    : Task(r, f) {}

    void initialize();
    void read();
    void actuate();
};


#endif //FLIGHT_SENSORARDUINO_HPP
