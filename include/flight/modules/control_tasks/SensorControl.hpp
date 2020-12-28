//
// Created by Srikar on 4/15/2020.
//

#ifndef FLIGHT_SENSORCONTROL_HPP
#define FLIGHT_SENSORCONTROL_HPP

#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>
#include <flight/modules/control_tasks/Control.hpp>
#include <flight/modules/lib/Kalman.hpp>
#include <vector>
#include <map>

class SensorControl : public Control {
private:
    double last_send_time;
    map<string, map<string, Kalman>> kalman_filters;

    void boundary_check();
    void send_sensor_data();

public:
    SensorControl();
    void begin() override;
    void execute() override;
};
#endif //FLIGHT_SENSORCONTROL_HPP
