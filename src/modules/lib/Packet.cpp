#include <map>
#include <flight/modules/lib/Util.hpp>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

void Packet::add(const Log& log) {
    logs.push_back(log);
}

string Packet::toString() const {
    // Convert all of the Logs to strings
    map<string, string> my_data;
    string logs_str = "[";

    for(const Log& log : logs){
        logs_str += log.toString();
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

Packet Packet::fromString(string inputString) {
    json j = json::parse(inputString);

    long timestamp = j.at("timestamp").get<long>();
    int level_int = j.at("log_priority").get<int>();
    auto log_priority = static_cast<LogPriority>(level_int);

    Packet packet = Packet(log_priority, timestamp);
    std::vector<json> logs = j.at("logs");
    for (json log : logs) {
        string header, message;
        long timestamp_;
        log.at("header").get_to(header);
        log.at("message").get_to(message);
        log.at("timestamp_").get_to(timestamp_);
        packet.add(Log(header, message, timestamp_));
    }

    // Create Packet object from input string
    // example inputString:
    // {"logs": ["{\"header\": \"heartbeat\", \"message\": \"AT\", \"timestamp\": 1608410538.3439176}"], "timestamp": 1608410538.3439176, "log_priority": 4}

    return packet;
}

vector<Log> Packet::getLogs() {
    return this->logs;
}
