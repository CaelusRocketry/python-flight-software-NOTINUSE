//
// Created by legoc on 12/27/2020.
//

#include <flight/modules/mcl/Config.hpp>

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
}
