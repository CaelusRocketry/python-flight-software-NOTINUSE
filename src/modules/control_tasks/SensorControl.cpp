//
// Created by adiv413 on 4/24/2020.
//

#include <flight/modules/control_tasks/SensorControl.hpp>

unordered_map<string, pair<int, int>> SensorControl::build_boundaries() {
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

SensorControl::SensorControl(Registry *registry, Flag *flag) {
    log("Sensor Control started");
    this->registry = registry;
    this->flag = flag;
    this->sensors = Util::parse_json({"sensors", "list"});
    this->send_interval = stod(Util::parse_json_value({"sensors", "send_interval"}));
    this->boundaries = build_boundaries();
    this->last_send_time = 0;
}

void SensorControl::begin() {

}

void SensorControl::execute() {
    boundary_check();
}

void SensorControl::boundary_check() {

}



