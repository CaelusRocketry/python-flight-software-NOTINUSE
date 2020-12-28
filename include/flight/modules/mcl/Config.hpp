//
// Created by myfatemi04 on 12/27/2020.
//

#include <nlohmann/json.hpp>

#ifndef FLIGHT_CONFIG_HPP
#define FLIGHT_CONFIG_HPP

using nlohmann::json;
using std::string;
using std::map;
using std::vector;

struct ConfigBoundary {
    double lower, upper;
};

void to_json(json& j, const ConfigBoundary& boundary) {
    j = json{{"lower", boundary.lower}, {"upper", boundary.upper}};
}

void from_json(const json& j, ConfigBoundary& boundary) {
    j.at("lower").get_to(boundary.lower);
    j.at("upper").get_to(boundary.upper);
}

struct ConfigSensorInfo {
    struct {
        double process_variance, measurement_variance, kalman_value;
    } kalman_args;
    struct {
        ConfigBoundary safe, warn;
    } boundaries;
    int pin;
};

void to_json(json& j, const ConfigSensorInfo& sensor_info) {
    json safe_boundaries, warn_boundaries;
    to_json(safe_boundaries, sensor_info.boundaries.safe);
    to_json(warn_boundaries, sensor_info.boundaries.warn);

    j = json{
        {"kalman_args", {
            {"process_variance", sensor_info.kalman_args.process_variance},
            {"measurement_variance", sensor_info.kalman_args.measurement_variance},
            {"kalman_value", sensor_info.kalman_args.kalman_value}
        }},
        {"boundaries", {
            {"safe", safe_boundaries},
            {"warn", warn_boundaries}
        }},
        {"pin", sensor_info.pin},
    };
}

void from_json(const json& j, ConfigSensorInfo& sensor_info) {
    json kalman_args = j.at("kalman_args");
    kalman_args.at("process_variance").get_to(sensor_info.kalman_args.process_variance);
    kalman_args.at("measurement_variance").get_to(sensor_info.kalman_args.measurement_variance);
    kalman_args.at("kalman_value").get_to(sensor_info.kalman_args.kalman_value);

    j.at("boundaries").at("safe").get_to(sensor_info.boundaries.safe);
    j.at("boundaries").at("warn").get_to(sensor_info.boundaries.warn);
    j.at("pin").get_to(sensor_info.pin);
}

struct ConfigValveInfo {
    int pin;
    string natural_state;
    bool special;
};

void to_json(json& j, const ConfigValveInfo& valve_info) {
    j = json{
        {"pin", valve_info.pin},
        {"natural_state", valve_info.natural_state},
        {"special", valve_info.special}
    };
}

void from_json(const json& j, ConfigValveInfo& valve_info) {
    j.at("pin").get_to(valve_info.pin);
    j.at("natural_state").get_to(valve_info.natural_state);
    j.at("special").get_to(valve_info.special);
}

class Config {
public:
    /* Default constructor */
    Config() = default;

    /* Reads config from a JSON object */
    explicit Config(json& json);

    struct {
        string GS_IP;
        int GS_PORT;

        string SOCKETIO_HOST;
        int SOCKETIO_PORT;

        double DELAY;
    } telemetry;

    struct {
        map<string, map<string, ConfigSensorInfo>> list;
        string address;
        int baud;
        double send_interval;
    } sensors;

    struct {
        map<string, map<string, ConfigValveInfo>> list;
        string address;
        int baud;
        double send_interval;
    } valves;

    struct {
        vector<string> list;
        double request_interval;
        double send_interval;
    } stages;

    struct {
        double delay;
    } timer;

    struct {
        vector<string> active_stages;
    } pressure_control;

    string arduino_type;
};

Config global_config;

#endif //FLIGHT_CONFIG_HPP
