#include <map>
#include <flight/modules/lib/Util.hpp>
#include <flight/modules/lib/Packet.hpp>

void Packet::add(Log log){
    logs.push_back(log);
}

string Packet::toString(){
    // Convert all of the Logs to strings
    map<string, string> my_data;
    string logs_str = "[";

    for(size_t i = 0; i < logs.size(); i++){
        logs_str += logs[i].toString();
        logs_str += ",";
    }

    // get rid of the trailing comma and replace it with the closing ]
    logs_str[logs_str.size() - 1] = ']';

    // Create dictionary representing Packet object
    my_data.insert(pair<string, string>("logs", logs_str));
    my_data.insert(pair<string, string>("timestamp", to_string(timestamp)));
    my_data.insert(pair<string, string>("level", to_string(int(level))));
    return Util::map_to_string(my_data, ":", ",");
}

Packet Packet::fromString(string inputString){
    // Create Packet object from input string
    // example inputString:
    // {"logs": ["{\"header\": \"heartbeat\", \"message\": \"AT\", \"timestamp\": 1608410538.3439176}"], "timestamp": 1608410538.3439176, "level": 4}

    auto logs = Util::parse_json_list({"logs"});
    string message = Util::parse_json_value({"message"});
    long timestamp = stol(Util::parse_json_value({"timestamp"}));
    int level_int = stoi(Util::parse_json_value({"level"}));

    LogPriority level = static_cast<LogPriority>(level_int);
    Packet packet = Packet(level, timestamp);

    // Add all the Logs to the Packet
    for(string log_str : logs) {
        packet.add(Log::fromString(log_str));
    }

    return packet;
}

vector<Log> Packet::getLogs() {
    return this->logs;
}
