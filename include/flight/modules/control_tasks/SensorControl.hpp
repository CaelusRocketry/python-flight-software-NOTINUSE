//
// Created by Srikar on 4/15/2020.
//
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>
#include <flight/modules/lib/Util.hpp>
#include <flight/modules/control_tasks/Control.hpp>

#ifndef FLIGHT_SENSORCONTROL_HPP
#define FLIGHT_SENSORCONTROL_HPP

class SensorControl : public Control {
private:
    Registry *registry;
    Flag *flag;
    vector<string> sensors;
    unordered_map<string, pair<int, int>> boundaries;
    double send_interval;
    double last_send_time;

    unordered_map<string, pair<int, int>> build_boundaries();
    void boundary_check();
    void send_sensor_data();
    void init_kalman();

public:
    SensorControl(Registry *registry, Flag *flag);
    void begin();
    void execute();
};
#endif //FLIGHT_SENSORCONTROL_HPP
