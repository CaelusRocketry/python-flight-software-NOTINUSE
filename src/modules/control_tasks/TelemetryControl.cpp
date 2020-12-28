//
// Created by adiv413 on 4/24/2020.
//

#include <flight/modules/control_tasks/TelemetryControl.hpp>
#include <flight/modules/lib/Util.hpp>
#include <Logger/logger_util.h>
#include <queue>

using nlohmann::json;

//TODO: add custom packet enqueuing interface to gs???

TelemetryControl::TelemetryControl() {
    global_flag.log_info("response", {
        {"header", "info"},
        {"Description", "Telemetry Control started"}
    });
}

void TelemetryControl::begin() {
    log("Telemetry control: Beginning");
    telemetry.connect();
    make_functions();
}

// Store list of all commands that GS can send as functions, add the function pointers to the map and call when necessary
void TelemetryControl::make_functions() {
    log("Telemetry: Making Functions");
    this->functions.emplace("heartbeat", &TelemetryControl::heartbeat);
    this->functions.emplace("soft_abort", &TelemetryControl::soft_abort);
    this->functions.emplace("solenoid_actuate", &TelemetryControl::solenoid_actuate);
    this->functions.emplace("sensor_request", &TelemetryControl::sensor_request);
    this->functions.emplace("valve_request", &TelemetryControl::valve_request);
    this->functions.emplace("progress", &TelemetryControl::progress);
    this->functions.emplace("test", &TelemetryControl::test);
}

void TelemetryControl::execute() {
    log("Telemetry control: Executing");
    if (!global_registry.telemetry.status) {
        global_flag.telemetry.reset = true;
    } else {
        global_flag.telemetry.reset = false;
        auto &ingest_queue = global_registry.telemetry.ingest_queue;
        while (!ingest_queue.empty()) {
            Packet packet = ingest_queue.top();

            //TODO: figure out if log command is outdated
            for(const Log& log_ : packet.getLogs()) {
                json j;
                to_json(j, log_);
                log(j.dump());
                ingest(log_);
            }
        }
    }
}
void TelemetryControl::ingest(const Log& log) {
    string header = log.getHeader();
    json params = log.getMessage();

    // Make sure the function exists
    if (this->functions.find(header) == this->functions.end()) {
        throw INVALID_HEADER_ERROR();
    }

    auto function = this->functions.at(header);
    vector<string> argument_order = arguments.at(header);

    // TODO: change the packet format from gs to make it strings instead of enums

    if (argument_order.size() != params.size()) {
        throw PACKET_ARGUMENT_ERROR();
    }

    vector<string> param_values;

    try {
        for (const string& argument_name : argument_order) {
            param_values.push_back(params.at(argument_name).get<string>());
        }
    } catch (...) {
        global_flag.log_warning("invalid_argument", {{"message", "Invalid function arguments"}});
    }

    (this->*function)(param_values); // call function which maps to the GS command sent w/ all params necessary
}
void TelemetryControl::heartbeat(const vector<string>& args) {
    global_flag.log_info("heartbeat", {
        {"header", "heartbeat"},
        {"response", "OK"}
    });
}

void TelemetryControl::soft_abort(const vector<string>& args) {
    global_registry.general.soft_abort = true;
    global_flag.log_critical("response", {
        {"header", "Soft Abort"},
        {"Status", "Success"},
        {"Description", "Rocket is undergoing soft abort"}
    });
    global_flag.log_critical("mode", {
        {"header", "Soft Abort"},
        {"mode", "Soft Abort"}
    });
}
void TelemetryControl::solenoid_actuate(const vector<string>& args) {
    if (!global_registry.valve_exists("solenoid", args[0])) {
        global_flag.log_critical("Valve actuation",{
            {"header", "Valve actuation"},
            {"Status", "Failure"},
            {"Description", "Unable to find actuatable solenoid"},
            {"Valve location", args[0]}
        });
        throw INVALID_SOLENOID_ERROR();
    }

    int current_priority = int(global_registry.valves["solenoid"][args[0]].actuation_priority);

    if (int(valve_priority_map[args[2]]) < current_priority) {
        global_flag.log_critical("Valve actuation", {
            {"header", "Valve actuation"},
            {"Status", "Failure"},
            {"Description", "Priority too low to actuate"},
            {"Valve location", args[0]},
            {"Actuation type", args[1]},
            {"Priority", args[2]}
        });
        throw INSUFFICIENT_PRIORITY_SOLENOID_ERROR();
    }

    log("Actuating solenoid at " + args[0] + " with actuation type " + args[1]);

    try {
        //TODO: make sure gs packets have the upper case version of the enum as the value for the actuation type
        FlagValveInfo &valve_flag = global_flag.valves["solenoid"][args[0]];
        valve_flag.actuation_type = actuation_type_map[args[1]];
        valve_flag.actuation_priority = valve_priority_map[args[2]];
    } catch(...) {
        global_flag.log_critical("Valve actuation", {
            {"header", "Valve actuation"},
            {"Status", "Failure"},
            {"Description", "Wrong packet message"},
            {"Valve location", args[0]},
            {"Actuation type", args[1]},
            {"Priority", args[2]}
        });
        throw INVALID_PACKET_MESSAGE_ERROR();
    }

    global_flag.log_info("Valve actuation", {
        {"header", "Valve actuation"},
        {"Status", "Success"},
        {"Description", "Successfully activated solenoid"}
    });
}

void TelemetryControl::sensor_request(const vector<string>& args) {
    double value;
    double kalman_value;
    string sensor_status_str;
    string sensor_type = args[0];
    string sensor_loc = args[1];

    if (!global_registry.sensor_exists(sensor_type, sensor_loc)) {
        global_flag.log_critical("response", {
            {"header", "Sensor data"},
            {"Status", "Failure"},
            {"Description", "Unable to find sensor"},
            {"Sensor type", args[0]},
            {"Sensor location", args[1]}
        });

        throw INVALID_SENSOR_LOCATION_ERROR();
    }

    auto sensor = global_registry.sensors[sensor_type][sensor_loc];
    value = sensor.measured_value;
    kalman_value = sensor.normalized_value;
    sensor_status_str = sensor_status_map[sensor.status];

    global_flag.log_critical("response", {
        {"header", "Sensor data request"},
        {"Status", "Success"},
        {"Sensor type", args[0]},
        {"Sensor location", args[1]},
        {"Sensor status", sensor_status_str},
        {"Measured value", value},
        {"Normalized value", kalman_value},
        {"Last updated", std::chrono::system_clock::now().time_since_epoch().count()}
    });
}
void TelemetryControl::valve_request(const vector<string>& args) {
    string state;
    string actuation_type;
    string actuation_priority;
    string valve_type = args[0];
    string valve_loc = args[1];

    if (!global_registry.valve_exists(valve_type, valve_loc)) {
        global_flag.log_critical("response", {
            {"header", "Valve data request"},
            {"Status", "Failure"},
            {"Description", "Unable to find valve"},
            {"Valve type", valve_type},
            {"Valve location", valve_loc}
        });
        throw INVALID_VALVE_LOCATION_ERROR();
    }

    auto valve_registry = global_registry.valves[valve_type][valve_loc];

    actuation_type = actuation_type_inverse_map.at(valve_registry.actuation_type);
    actuation_priority = valve_priority_inverse_map.at(valve_registry.actuation_priority);

    global_flag.log_critical("response", {
        {"header", "Valve data request"},
        {"Status", "Success"},
        {"Actuation type", actuation_type},
        {"Actuation priority", actuation_priority},
        {"Valve type", valve_type},
        {"Valve location", valve_loc},
        {"Last actuated", std::chrono::system_clock::now().time_since_epoch().count()}
    });
}
void TelemetryControl::progress(const vector<string>& args) {
    global_flag.general.progress = true;
}
void TelemetryControl::test(const vector<string>& args) {
    log("Test received: " + args[0]);
}