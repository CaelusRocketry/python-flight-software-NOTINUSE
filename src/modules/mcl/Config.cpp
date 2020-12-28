//
// Created by legoc on 12/27/2020.
//

#include <flight/modules/mcl/Config.hpp>

/* BOUNDARY JSON SERIALIZATION */

void to_json(json& j, const ConfigBoundary& boundary) {
    j = json{{"lower", boundary.lower}, {"upper", boundary.upper}};
}

void from_json(const json& j, ConfigBoundary& boundary) {
    j.at("lower").get_to(boundary.lower);
    j.at("upper").get_to(boundary.upper);
}

/* SENSOR JSON SERIALIZATION */

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

/* VALVE JSON SERIALIZATION */

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

using nlohmann::json;

Config::Config(json& json) {
    /* Read telemetry */
    telemetry.GS_IP = json["telemetry"]["GS_IP"];
    telemetry.GS_PORT = json["telemetry"]["GS_PORT"];
    telemetry.DELAY = json["telemetry"]["DELAY"];
    telemetry.SOCKETIO_HOST = json["telemetry"]["SOCKETIO_HOST"];
    telemetry.SOCKETIO_PORT = json["telemetry"]["SOCKETIO_PORT"];

    /* Read sensor list */
    json["sensors"]["list"].get_to(sensors.list);
    sensors.address = json["sensors"]["address"];
    sensors.baud = json["sensors"]["baud"];
    sensors.send_interval = json["sensors"]["send_interval"];

    /* Read valve list */
    json["valves"]["list"].get_to(valves.list);
    valves.address = json["valves"]["address"];
    valves.baud = json["valves"]["baud"];
    valves.send_interval = json["valves"]["send_interval"];

    /* Read stage list */
    // Needs to be done indirectly because of = operator overloading
    json["stages"]["list"].get_to(stages.list);
    stages.request_interval = json["stages"]["request_interval"];
    stages.send_interval = json["stages"]["send_interval"];

    /* Read timer config */
    timer.delay = json["timer"]["delay"];

    /* Read pressure control stages list */
    vector<string> pressure_control__active_stages = json["pressure_control"]["active_stages"];
    pressure_control.active_stages = pressure_control__active_stages;

    /* Read arduino type */
    arduino_type = json["arduino_type"];

    /* Read task config */
    json.at("task_config").at("tasks").get_to(task_config.tasks);
    json.at("task_config").at("control_tasks").get_to(task_config.control_tasks);
}

// Define the value declared with extern in the header file
Config global_config;
