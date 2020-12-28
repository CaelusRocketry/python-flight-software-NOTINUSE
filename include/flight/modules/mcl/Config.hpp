//
// Created by myfatemi04 on 12/27/2020.
//

#ifndef FLIGHT_CONFIG_HPP
#define FLIGHT_CONFIG_HPP

#include <nlohmann/json.hpp>

using nlohmann::json;
using std::string;
using std::map;
using std::vector;

struct ConfigBoundary {
    double lower, upper;
};

void to_json(json& j, const ConfigBoundary& boundary);
void from_json(const json& j, ConfigBoundary& boundary);

struct ConfigSensorInfo {
    struct {
        double process_variance, measurement_variance, kalman_value;
    } kalman_args;
    struct {
        ConfigBoundary safe, warn;
    } boundaries;
    int pin;
};

void to_json(json& j, const ConfigSensorInfo& sensor_info);
void from_json(const json& j, ConfigSensorInfo& sensor_info);

struct ConfigValveInfo {
    int pin;
    string natural_state;
    bool special;
};

void to_json(json& j, const ConfigValveInfo& valve_info);
void from_json(const json& j, ConfigValveInfo& valve_info);

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

        int DELAY;
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
        double delay = 1;
    } timer;

    struct {
        vector<string> active_stages;
    } pressure_control;

    struct {
        vector<string> tasks, control_tasks;
    } task_config;

    string arduino_type;
};

extern Config global_config;

#endif //FLIGHT_CONFIG_HPP
