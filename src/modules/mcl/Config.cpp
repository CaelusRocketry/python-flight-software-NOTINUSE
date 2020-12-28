//
// Created by legoc on 12/27/2020.
//

#include <flight/modules/mcl/Config.hpp>
#include <Logger/logger_util.h>

/* BOUNDARY JSON SERIALIZATION */

void to_json(json& j, const ConfigBoundary& boundary) {
    j = json{boundary.lower, boundary.upper};
}

void from_json(const json& j, ConfigBoundary& boundary) {
    j[0].get_to(boundary.lower);
    j[1].get_to(boundary.upper);
}

/* SENSOR JSON SERIALIZATION */

void to_json(json& j, const ConfigSensorInfo& sensor_info) {
    j = json{
        {"kalman_args", {
            {"process_variance", sensor_info.kalman_args.process_variance},
            {"measurement_variance", sensor_info.kalman_args.measurement_variance},
            {"kalman_value", sensor_info.kalman_args.kalman_value}
        }},
        {"boundaries", {
            {"safe", sensor_info.boundaries.safe},
            {"warn", sensor_info.boundaries.warn}
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
        {"natural", valve_info.natural_state},
        {"special", valve_info.special}
    };
}

void from_json(const json& j, ConfigValveInfo& valve_info) {
    j.at("pin").get_to(valve_info.pin);
    j.at("natural").get_to(valve_info.natural_state);
    j.at("special").get_to(valve_info.special);
}

using nlohmann::json;

Config::Config(json& json) {
    log("Config: Initializing");

    log("Config: Reading telemetry data");
    /* Read telemetry */
    json.at("telemetry").at("GS_IP").get_to(telemetry.GS_IP);
    json.at("telemetry").at("GS_PORT").get_to(telemetry.GS_PORT);
    json.at("telemetry").at("DELAY").get_to(telemetry.DELAY);
    json.at("telemetry").at("SOCKETIO_HOST").get_to(telemetry.SOCKETIO_HOST);
    json.at("telemetry").at("SOCKETIO_PORT").get_to(telemetry.SOCKETIO_PORT);

    log("Config: Reading sensor list");
    /* Read sensor list */
    json.at("sensors").at("list").get_to(sensors.list);
    json.at("sensors").at("address").get_to(sensors.address);
    json.at("sensors").at("baud").get_to(sensors.baud);
    json.at("sensors").at("send_interval").get_to(sensors.send_interval);

    log("Config: Reading valve list");
    /* Read valve list */
    json.at("valves").at("list").get_to(valves.list);
    json.at("valves").at("address").get_to(valves.address);
    json.at("valves").at("baud").get_to(valves.baud);
    json.at("valves").at("send_interval").get_to(valves.send_interval);

    log("Config: Reading stage list");
    /* Read stage list */
    json.at("stages").at("list").get_to(stages.list);
    json.at("stages").at("request_interval").get_to(stages.request_interval);
    json.at("stages").at("send_interval").get_to(stages.send_interval);

    log("Config: Reading timer config");
    /* Read timer config */
    json.at("timer").at("delay").get_to(timer.delay);

    log("Config: Reading pressure control stages list");
    /* Read pressure control stages list */
    json.at("pressure_control").at("active_stages").get_to(pressure_control.active_stages);

    log("Config: Reading arduino type");
    /* Read arduino type */
    json.at("arduino_type").get_to(arduino_type);

    log("Config: Reading task config");
    /* Read task config */
    json.at("task_config").at("tasks").get_to(task_config.tasks);
    json.at("task_config").at("control_tasks").get_to(task_config.control_tasks);
}

// Define the value declared with extern in the header file
Config global_config;
