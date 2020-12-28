//
// Created by adiv413 on 4/24/2020.
//

#include <flight/modules/control_tasks/TelemetryControl.hpp>
#include <flight/modules/lib/Util.hpp>
#include <queue>

//TODO: add custom packet enqueuing interface to gs???

TelemetryControl::TelemetryControl() {
    global_flag.log_info("response", "{\"header\": \"info\", \"Description\": \"Telemetry Control started\"}");
}

// Store list of all commands that GS can send as functions, add the function pointers to the map and call when necessary
void TelemetryControl::makeFunctions() {
    this->functions.emplace("heartbeat", &TelemetryControl::heartbeat);
    this->functions.emplace("soft_abort", &TelemetryControl::soft_abort);
    this->functions.emplace("solenoid_actuate", &TelemetryControl::solenoid_actuate);
    this->functions.emplace("sensor_request", &TelemetryControl::sensor_request);
    this->functions.emplace("valve_request", &TelemetryControl::valve_request);
    this->functions.emplace("progress", &TelemetryControl::progress);
    this->functions.emplace("test", &TelemetryControl::test);
}

void TelemetryControl::begin() {
    makeFunctions();
}
void TelemetryControl::execute() {
    if (!global_registry.telemetry.status) {
        global_flag.telemetry.reset = true;
    } else {
        global_flag.telemetry.reset = false;
        auto &ingest_queue = global_registry.telemetry.ingest_queue;
        while (!ingest_queue.empty()) {
            Packet packet = ingest_queue.top();

            //TODO: figure out if log command is outdated
            for(const Log& log_ : packet.getLogs()) {
                log(log_.toString());
                ingest(log_);
            }
        }
    }
}
void TelemetryControl::ingest(Log log) {
    string header = log.getHeader();
    if(this->functions.find(header) != this->functions.end()) {
        auto function = this->functions.at(header);
        auto params = Util::string_to_map(log.getMessage(), ":", ",");
        vector<string> param_values;

        if(arguments.size() != params.size()) {
            throw PACKET_ARGUMENT_ERROR();
        }

        auto x = arguments.at(header);

        //TODO: change the packet format from gs to make it strings instead of enums

        for(auto vector_it = x.begin(); vector_it != x.end(); vector_it++) {
            for(auto param : params) {
                if((*vector_it) != param.first) {
                    //throw error, wrong message format
                } else {
                    param_values.push_back(param.second);
                }
            }
        }

        (this->*function)(param_values); // call function which maps to the GS command sent w/ all params necessary
    }
    else {
        throw INVALID_HEADER_ERROR();
    }
}
void TelemetryControl::heartbeat(vector<string> args) {
    global_flag.log_info("heartbeat", "{\"header\": \"heartbeat\", \"response\": \"OK\"}");
}

void TelemetryControl::soft_abort(vector<string> args) {
    global_registry.general.soft_abort = true;
    global_flag.log_critical("response", "{\"header\": \"Soft abort\", \"Status\": \"Success\", \"Description\": \"Rocket is undergoing soft abort\"}");
    global_flag.log_critical("mode", "{\"header\": \"Soft abort\", \"mode\": \"Soft abort\"}");
}
void TelemetryControl::solenoid_actuate(vector<string> args) {
    int current_priority;
    try {
        current_priority = int(global_registry.valves["solenoid"][args[0]].actuation_priority);
    } catch(...) {
        global_flag.log_critical("Valve actuation", "{\"header\": \"Valve actuation\", \"Status\": \"Failure\", \"Description\": \"Unable to find actuatable solenoid\", \"Valve location\": \"" + args[0] + "\"}");
        throw INVALID_SOLENOID_ERROR();
    }

    if (int(valve_priority_map[args[2]]) < current_priority) {
        global_flag.log_critical("Valve actuation", "{\"header\": \"Valve actuation\", \"Status\": \"Failure\", \"Description\": \"Too little priority to actuate solenoid\", \"Valve location\": \"" + args[0] + "\", \"Actuation type\": \"" + args[1] + "\", \"Priority\": \"" + args[2] + "\"}");
        throw INSUFFICIENT_PRIORITY_SOLENOID_ERROR();
    }

    log("Actuating solenoid at " + args[0] + " with actuation type " + args[1]);

    try {
        //TODO: make sure gs packets have the upper case version of the enum as the value for the actuation type
        FlagValveInfo &valve_flag = global_flag.valves["solenoid"][args[0]];
        valve_flag.actuation_type = actuation_type_map[args[1]];
        valve_flag.actuation_priority = valve_priority_map[args[2]];
    } catch(...) {
        global_flag.log_critical("Valve actuation", "{\"header\": \"Valve actuation\", \"Status\": \"Failure\", \"Description\": \"Wrong packet message\", \"Valve location\": \"" + args[0] + "\", \"Actuation type\": \"" + args[1] + "\", \"Priority\": \"" + args[2] + "\"}");
        throw INVALID_PACKET_MESSAGE_ERROR();
    }

    global_flag.log_info("Valve actuation", "{\"header\": \"Valve actuation\", \"Status\": \"Success\", \"Description\": \"Successfully actuated solenoid\"}");
}
void TelemetryControl::sensor_request(vector<string> args) {
    double value;
    double kalman_value;
    string sensor_status_str;
    string sensor_type = args[0];
    string sensor_loc = args[1];
    auto sensor = global_registry.sensors[sensor_type][sensor_loc];
    try {
        value = sensor.measured_value;
        kalman_value = sensor.normalized_value;
        sensor_status_str = sensor_status_map[sensor.status];
    } catch(...) {
        global_flag.log_critical("response", "{\"header\": \"Sensor data\", \"Status\": \"Failure\", \"Description\": \"Unable to find sensor\", \"Type\": \"" + args[0] + ", \"Location\": \"" + args[1] + "}");
        throw INVALID_SENSOR_LOCATION_ERROR();
    }

    auto now = std::chrono::system_clock::now().time_since_epoch().count();
    global_flag.log_critical("response", "{\"header\": \"sensor_data_request\", \"Status\": \"Success\", \"Sensor type\": \"" +
        sensor_type + "\", \"Sensor location\": \"" + sensor_loc + ", \"Measured value\": \"" + to_string(value) +
        ", \"Normalized value\": \"" + to_string(kalman_value) + ", \"Sensor status\": \"" + sensor_status_str +
        ", \"Last updated\": \"" + to_string(now) + "}");
}
void TelemetryControl::valve_request(vector<string> args) {
    string state;
    string actuation_type;
    string actuation_priority;
    string valve_type = args[0];
    string valve_loc = args[1];
    auto valve_registry = global_registry.valves[valve_type][valve_loc];

    try {
        state = solenoid_state_map.at(valve_registry.state);
        actuation_type = actuation_type_inverse_map.at(valve_registry.actuation_type);
        actuation_priority = valve_priority_inverse_map.at(valve_registry.actuation_priority);
    } catch(...) {
        global_flag.log_critical("response", "{\"header\": \"valve_data_request\", \"Status\": \"Failure\", \"Description\": \"Unable to find valve\", \"Valve type\": \"" + valve_type + ", \"Valve location\": \"" + valve_loc + "}");
        throw INVALID_VALVE_LOCATION_ERROR();
    }

    auto now = std::chrono::system_clock::now().time_since_epoch().count();

    global_flag.log_critical("response", "{\"header\": \"valve_data_request\", \"Status\": \"Success\", "
        "\"Type\": \"" + valve_type + "\", \"Location\": \"" + valve_loc + ", \"State\": \"" + state + ", \"Actuation type\": \"" +
        actuation_type + ", \"Actuation priority\": \"" + actuation_priority + ", \"Last actuated\": \"" +
        to_string(now) + "}");
}
void TelemetryControl::progress(vector<string> args) {
    global_flag.general.progress = true;
}
void TelemetryControl::test(vector<string> args) {
    log("Test received: " + args[0]);
}