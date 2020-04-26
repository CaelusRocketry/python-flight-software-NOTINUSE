//
// Created by adiv413 on 4/24/2020.
//

#include <flight/modules/control_tasks/SensorControl.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <boost/any.hpp>
#include <chrono>

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
}

void SensorControl::begin() {
    this->sensors = build_sensors();
    this->send_interval = stod(Util::parse_json_value({"sensors", "send_interval"}));
    this->boundaries = build_boundaries();
    this->kalman_filters = init_kalman();
    log("Sensor Control started");
}

void SensorControl::execute() {
    boundary_check();

    if(last_send_time == 0 || chrono::system_clock::now().time_since_epoch().count() - last_send_time > send_interval) {
        send_sensor_data();
        last_send_time = chrono::system_clock::now().time_since_epoch().count();
    }
}

void SensorControl::boundary_check() {
    vector<string> crits;

    for(string &sensor : sensors) {
        double value = registry->get<double>("sensor_normalized." + sensor);
        double kalman_value = kalman_filters.at(sensor).update_kalman(value);
        this->registry->put("sensor_normalized." + sensor, kalman_value);

        if (boundaries.at(sensor + ".safe").first <= kalman_value <= boundaries.at(sensor + ".safe").second) {
            registry->put("sensor_status." + sensor, SensorStatus::SAFE);
        } else if (boundaries.at(sensor + ".warn").first <= kalman_value <= boundaries.at(sensor + ".warn").second) {
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
               log("Sensors have returned to normal"); //TODO: change to enqueue once telemetry is done
           }
        }
        else if(!soft){ //one or more of the sensors are critical, soft abort if we haven't already done so
            registry->put("general.soft_abort", true);

            //TODO: change to enqueue once telemetry is done

            log("Soft aborting because the following sensors have reached critical levels:");

            for(string &x : crits) {
                log("\t" + x);
            }
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
    for(string &sensor : sensors) {
        double value = registry->get<double>("sensor_measured." + sensor);
        double kalman_value = registry->get<double>("sensor_normalized." + sensor);

        //TODO: make this work, rn registry cant do get with enums???
        //SensorStatus status = registry->get<SensorStatus>("sensor_status." + sensor);

        //TODO: replace with enqueue once telemetry is done

        log(sensor + " - normal: " + to_string(value) + " kalman: " + to_string(kalman_value) + " status: " + sensor_status_names.at(3));
    }
}

