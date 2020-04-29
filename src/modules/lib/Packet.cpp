#include <map>
#include <flight/modules/lib/Util.hpp>
#include <flight/modules/lib/Packet.hpp>

void Packet::add(Log log){
    logs.push_back(log);
}

string Packet::toString(){
    // Convert all of the Logs to strings
    map<string, string> my_data;
    string logs_str = "";
    for(size_t i = 0; i < logs.size(); i++){
        logs_str += logs[i].toString();
        logs_str += "|";
    }

    // Create dictionary representing Packet object
    my_data.insert(pair<string, string>("logs", logs_str));
    my_data.insert(pair<string, string>("timestamp", to_string(timestamp)));
    my_data.insert(pair<string, string>("level", to_string(int(level))));
    return Util::map_to_string(my_data, ":", "\n");
}

Packet Packet::fromString(string inputString){
    // Create Packet object from input string
    map<string, string> data = Util::string_to_map(inputString, ":", "\n");
    long timestamp = stol(data["timstamp"]);
    LogPriority level = static_cast<LogPriority>(stoi(data["timstamp"]));
    Packet packet = Packet(level, timestamp);

    // Add all the Logs to the Packet
    string logs_str = data["logs"];
    size_t pos;
    string delim = "|";
    while((pos = logs_str.find(delim)) != string::npos){
        string log_str = logs_str.substr(0, pos);
        packet.add(Log::fromString(log_str));
        logs_str.erase(0, pos + delim.length());
    }
    return packet;
}

