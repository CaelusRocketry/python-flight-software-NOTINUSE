//
// Created by Srikar on 4/15/2020.
//
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>
#include <flight/modules/control_tasks/Control.hpp>
#include <flight/modules/lib/Kalman.hpp>
#include <vector>

#ifndef FLIGHT_SENSORCONTROL_HPP
#define FLIGHT_SENSORCONTROL_HPP

class SensorControl : public Control {
private:
    Registry *registry;
    Flag *flag;
    vector<string> sensors;
    unordered_map<string, pair<double, double>> boundaries;
    double send_interval;
    double last_send_time;
    unordered_map<string, Kalman> kalman_filters;
    const vector<string> sensor_status_names = {"", "CRITICAL", "WARNING", "SAFE"};

    unordered_map<string, pair<double, double>> build_boundaries();
    vector<string> build_sensors();
    void boundary_check();
    void send_sensor_data();
    unordered_map<string, Kalman> init_kalman();

public:
    SensorControl(Registry *registry, Flag *flag);
    void begin();
    void execute();
};
#endif //FLIGHT_SENSORCONTROL_HPP
