//
// Created by Srikar on 4/15/2020.
//
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>
#include <flight/modules/lib/Util.hpp>

#ifndef FLIGHT_SENSORCONTROL_HPP
#define FLIGHT_SENSORCONTROL_HPP

class SensorControl {
private:
    Registry registry;
    Flag flag;
    vector<string> sensors;
    unordered_map<string, pair<int, int>> boundaries;
    double send_interval;
    double last_send_time = 0;

    //TODO: is there a better way to implement this?
    unordered_map<string, pair<int, int>> build_boundaries() {
        unordered_map<string, pair<int, int>> ret;

        for(string i : Util::parse_json({"boundaries"})) {
            for(string j : Util::parse_json({"boundaries", i})) {
                for(string k : Util::parse_json({"boundaries", i, j})) {
                    auto values = Util::parse_json_list({"boundaries", i, j, k});
                    ret[i + "." + j + "." + k] = make_pair(stod(values.at(0)), stod(values.at(1)));
                }
            }
        }

        return ret;
    }

    void boundary_check() {

    }

    void send_sensor_data() {

    }

    void init_kalman() {

    }

public:
    SensorControl(Registry registry, Flag flag) {
        log("Sensor Control started");
        this->registry = registry;
        this->flag = flag;
        this->sensors = Util::parse_json({"sensors", "list"});
        this->send_interval = stod(Util::parse_json_value({"sensors", "send_interval"}));
        this->boundaries = build_boundaries();
    }

    void execute() {
        boundary_check();

    }
};
#endif //FLIGHT_SENSORCONTROL_HPP
