//
// Created by adiv413 on 4/24/2020.
//

#include <flight/modules/control_tasks/SensorControl.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <flight/modules/lib/Util.hpp>
#include <boost/any.hpp>
#include <chrono>

// Reads the sensor boundaries from config and stores them in a map

unordered_map<string, pair<double, double>> SensorControl::build_boundaries() {
    unordered_map<string, pair<double, double>> ret;

    for(string &i : Util::parse_json({"boundaries"})) {
        for(string &j : Util::parse_json({"boundaries", i})) {
            for(string &k : Util::parse_json({"boundaries", i, j})) {
                auto values = Util::parse_json_list({"boundaries", i, j, k});
                ret[i + "." + j + "." + k] = make_pair(stod(values.at(0)), stod(values.at(1)));
            }
        }
    }

    return ret;
}

SensorControl::SensorControl(Registry *registry, Flag *flag) {
    this->registry = registry;
    this->flag = flag;
    this->last_send_time = 0;
    Util::enqueue(this->flag, Log("response", "{\"header\": \"info\", \"Description\": \"Sensor Control started\"}"), LogPriority::INFO);
}

void SensorControl::begin() {
    this->sensors = build_sensors();
    this->send_interval = stod(Util::parse_json_value({"sensors", "send_interval"}));
    this->boundaries = build_boundaries();
    this->kalman_filters = init_kalman();
}

void SensorControl::execute() {
    boundary_check();

    if(last_send_time == 0 || chrono::system_clock::now().time_since_epoch().count() - last_send_time > send_interval) {
        send_sensor_data();
        last_send_time = chrono::system_clock::now().time_since_epoch().count();
    }
}

void SensorControl::boundary_check() {
    /*
     * Sensor paths in registry are stred as the following:
     * sensor_[measured/normalized/status]
     */
    vector<string> crits;

    for(string &sensor : sensors) {
        double value = registry->get<double>("sensor_measured." + sensor);
        double kalman_value = kalman_filters.at(sensor).update_kalman(value);
        this->registry->put("sensor_normalized." + sensor, kalman_value);

        if (boundaries.at(sensor + ".safe").first <= kalman_value && kalman_value <= boundaries.at(sensor + ".safe").second) {
            registry->put("sensor_status." + sensor, SensorStatus::SAFE);
        } else if (boundaries.at(sensor + ".warn").first <= kalman_value && kalman_value <= boundaries.at(sensor + ".warn").second) {
            registry->put("sensor_status." + sensor, SensorStatus::WARNING);
        } else {
            registry->put("sensor_status." + sensor, SensorStatus::CRITICAL);
            crits.push_back(sensor);
        }
    }

    bool hard = registry->get<bool>("general.hard_abort");
    bool soft = registry->get<bool>("general.soft_abort");

    if(!hard) {
        if(crits.empty()) {
           if(soft) { //undo soft abort
               registry->put("general.soft_abort", false);
               Util::enqueue(this->flag, Log("response", "{\"header\": \"info\", \"Description\": \"Sensors have returned to normal\"}"), LogPriority::CRIT);
           }
        }
        else if(!soft){ //one or more of the sensors are critical, soft abort if we haven't already done so
            registry->put("general.soft_abort", true);
            string message = "Soft aborting because the following sensors have reached critical levels- ";

            for(string &x : crits) {
                message += x + ", ";
            }
            message = message.substr(0, message.length() - 2);
            Util::enqueue(this->flag, Log("response", "{\"header\": \"info\", \"Description\": \"" + message + "\"}"), LogPriority::CRIT);
        }
    }
}

unordered_map<string, Kalman> SensorControl::init_kalman() {
    unordered_map<string, Kalman> ret;

    for(string &sensor : sensors) {
        int delim = sensor.find(".");
        double process_variance = stod(Util::parse_json_value({
                    "kalman_args",
                    sensor.substr(0, delim),
                    sensor.substr(delim + 1, sensor.length()),
                    "process_variance"
                }));
        double measurement_variance = stod(Util::parse_json_value({
                    "kalman_args",
                    sensor.substr(0, delim),
                    sensor.substr(delim + 1, sensor.length()),
                    "measurement_variance"
                }));
        double kalman_value = stod(Util::parse_json_value({
                    "kalman_args",
                    sensor.substr(0, delim),
                    sensor.substr(delim + 1, sensor.length()),
                    "kalman_value"
                }));
        ret.insert({sensor, Kalman(process_variance, measurement_variance, kalman_value)});
    }

    return ret;
}

vector<string> SensorControl::build_sensors() {
    vector<string> ret;
    for(string &i : Util::parse_json({"sensors", "list"})) {
        for(string &j : Util::parse_json_list({"sensors", "list", i})) {
            ret.push_back(i + "." + j);
        }
    }

    return ret;
}

void SensorControl::send_sensor_data() {
    string message = "{";

    for(string &sensor : sensors) {
        double value = registry->get<double>("sensor_measured." + sensor);
        double kalman_value = registry->get<double>("sensor_normalized." + sensor);

        SensorStatus status = registry->get<SensorStatus>("sensor_status." + sensor);

        message += "\"" + sensor + "\": {";
        message += "\"measured\": " + to_string(value) + ", \"kalman\": " + to_string(kalman_value) + ", \"status\": " + sensor_status_names.at(int(status));
        message += "}, ";
    }

    Util::enqueue(this->flag, Log("sensor_data", message), LogPriority::INFO);
}

