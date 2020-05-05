//
// Created by adiv413 on 4/24/2020.
//

#include <flight/modules/control_tasks/TelemetryControl.hpp>
#include <flight/modules/lib/Packet.hpp>
#include <flight/modules/lib/Util.hpp>
#include <queue>

//TODO: add custom packet enqueuing interface to gs???

typedef priority_queue<Packet, vector<Packet>, Packet::compareTo> PacketQueue;

TelemetryControl::TelemetryControl(Registry *registry, Flag *flag) {
    log("Telemetry Control started");
    this->registry = registry;
    this->flag = flag;
}
void TelemetryControl::makeFunctions() {
    this->functions.emplace("heartbeat", &TelemetryControl::heartbeat);
    this->functions.emplace("hard_abort", &TelemetryControl::hard_abort);
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
    bool status = this->registry->get<bool>("telemetry.status");
    if(!status) {
        this->flag->put("telemetry.reset", true);
    }
    else {
        this->flag->put("telemetry.reset", false);
        PacketQueue ingest_queue = this->registry->get<PacketQueue>("telemetry.ingest_queue");
        while(!ingest_queue.empty()) {
            Packet packet = ingest_queue.top();

            //TODO: figure out if log command is outdated
            for(Log l : packet.getLogs()) {
                log(l.toString());
                ingest(l);
            }
        }

        this->registry->put("telemetry.ingest_queue", PacketQueue());
    }
}
void TelemetryControl::ingest(Log log) {
    string header = log.getHeader();
    if(this->functions.find(header) != this->functions.end()) {
        auto function = this->functions.at(header);
        auto params = Util::string_to_map(log.getMessage(), ":", ",");
        vector<string> param_values;

        if(arguments.size() != params.size()) {
            //TODO: throw error or smth
        }

        auto x = arguments.at(header);

        //TODO: change the packet format from gs to make it strings instead of enums

        for(auto vector_it = x.begin(); vector_it != x.end(); vector_it++) {
            for(auto param : params) {
                if((*vector_it).compare(param.first) != 0) {
                    //throw error, wrong message format
                }
                else {
                    param_values.push_back(param.second);
                }
            }
        }

        (this->*function)(param_values);
    }
    else {
        //TODO: throw error, invalid header
    }
}
void TelemetryControl::heartbeat(vector<string> args) {
    Util::enqueue(this->flag, Log("heartbeat", "{\"header\": \"heartbeat\", \"response\": \"OK\"}"), LogPriority::INFO);
}
void TelemetryControl::hard_abort(vector<string> args) {
    this->registry->put("general.hard_abort", true);
    Util::enqueue(this->flag, Log("response", "{\"header\": \"Hard abort\", \"Status\": \"Success\", \"Description\": \"Rocket is undergoing hard abort\"}"), LogPriority::CRIT);
    Util::enqueue(this->flag, Log("mode", "{\"header\": \"Hard abort\", \"mode\": \"Hard abort\"}"), LogPriority::CRIT);
}
void TelemetryControl::soft_abort(vector<string> args) {
    this->registry->put("general.soft_abort", true);
    Util::enqueue(this->flag, Log("response", "{\"header\": \"Soft abort\", \"Status\": \"Success\", \"Description\": \"Rocket is undergoing soft abort\"}"), LogPriority::CRIT);
    Util::enqueue(this->flag, Log("mode", "{\"header\": \"Soft abort\", \"mode\": \"Soft abort\"}"), LogPriority::CRIT);
}
void TelemetryControl::solenoid_actuate(vector<string> args) {
    int current_priority;
    try {
        current_priority = int(this->registry->get<ValvePriority>("valve_actuation_priority.solenoid." + args[0]));
    }
    catch(...) {
        Util::enqueue(this->flag, Log("Valve actuation", "{\"header\": \"Valve actuation\", \"Status\": \"Failure\", \"Description\": \"Unable to find actuatable solenoid\", \"Valve location\": \"" + args[0] + "\"}"), LogPriority::CRIT);
        //TODO: throw error
    }

    if(int(valve_priority_map[args[2]]) < current_priority) {
        Util::enqueue(this->flag, Log("Valve actuation", "{\"header\": \"Valve actuation\", \"Status\": \"Failure\", \"Description\": \"Too little priority to actuate solenoid\", \"Valve location\": \"" + args[0] + "\", \"Actuation type\": \"" + args[1] + "\", \"Priority\": \"" + args[2] + "\"}"), LogPriority::CRIT);
        //TODO: throw error
    }

    log("Actuating solenoid at " + args[0] + " with actuation type " + args[1]);

    try {
        //TODO: make sure gs packets have the upper case version of the enum as the value for the actuation type
        this->flag->put("valve_actuation_type.solenoid." + args[0], actuation_type_map[args[1]]);
        this->flag->put("valve_actuation_priority.solenoid." + args[0], valve_priority_map[args[2]]);
    }
    catch(...) {
        Util::enqueue(this->flag, Log("Valve actuation", "{\"header\": \"Valve actuation\", \"Status\": \"Failure\", \"Description\": \"Wrong packet message\", \"Valve location\": \"" + args[0] + "\", \"Actuation type\": \"" + args[1] + "\", \"Priority\": \"" + args[2] + "\"}"), LogPriority::CRIT);
        //TODO: throw error
    }

    Util::enqueue(this->flag, Log("Valve actuation", "{\"header\": \"Valve actuation\", \"Status\": \"Success\", \"Description\": \"Successfully actuated solenoid\"}"), LogPriority::CRIT);
}
void TelemetryControl::sensor_request(vector<string> args) {
    double value;
    double kalman_value;
    string sensor_status;
    try {
        value = this->registry->get<double>("sensor_measured." + args[0] + "." + args[1]);
        kalman_value = this->registry->get<double>("sensor_normalized." + args[0] + "." + args[1]);
        sensor_status = sensor_status_map[this->registry->get<SensorStatus>("sensor_status." + args[0] + "." + args[1])];
    }
    catch(...) {
        Util::enqueue(this->flag, Log("response", "{\"header\": \"Sensor data\", \"Status\": \"Failure\", \"Description\": \"Unable to find sensor\", \"Type\": \"" + args[0] + ", \"Location\": \"" + args[1] + "}"), LogPriority::CRIT);
        //TODO: throw error
    }
    Util::enqueue(this->flag, Log("response", "{\"header\": \"Sensor data\", \"Status\": \"Success\", \"Sensor type\": \"" +
        args[0] + "\", \"Sensor location\": \"" + args[1] + ", \"Measured value\": \"" + to_string(value) +
        ", \"Normalized value\": \"" + to_string(kalman_value) + ", \"Sensor status\": \"" + sensor_status +
        ", \"Last updated\": \"" + to_string(std::chrono::system_clock::now().time_since_epoch().count()) + "}"), LogPriority::CRIT);
}
void TelemetryControl::valve_request(vector<string> args) {

}
void TelemetryControl::progress(vector<string> args) {
    this->flag->put("general.progress", true);
}
void TelemetryControl::test(vector<string> args) {
    log("Test received: " + args[0]);
}