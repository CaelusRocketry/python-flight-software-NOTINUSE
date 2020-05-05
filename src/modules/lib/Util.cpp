#include <flight/modules/lib/Util.hpp>
#include <queue>

namespace pt = boost::property_tree;
vector<string> Util::parse_json(initializer_list<string> args) {
    pt::ptree root;
    pt::read_json("../src/config.json", root);
    auto item = root;
    vector<string> ret;

    if(args.size() == 0) {
        log("error: no arguments to parse json"); //TODO: send message to gs
        return vector<string>();
    }

    try {
        for (string s : args) {
            item = item.get_child(s);
        }
        for (auto &sub_item : item) {
            ret.push_back(sub_item.first);
        }
    }
    catch (...) {
        log("error occurred while parsing json"); //TODO: send message to gs
        return vector<string>();
    }

    return ret;
}

/*
 * Example: to get a list of all the solenoids, do parse_json_list({"valves", "list", "solenoid"}).
 * Note that you have to specify the field "solenoid" in order to get the items from the list.
 */

vector<string> Util::parse_json_list(initializer_list<string> args) {
    pt::ptree root;
    pt::read_json("../src/config.json", root);
    auto item = root;
    vector<string> ret;

    if(args.size() == 0) {
        log("error: no arguments to parse json"); //TODO: send message to gs
        return vector<string>();
    }

    try {
        for (string s : args) {
            item = item.get_child(s);
        }
        for (auto &sub_item : item) {
            ret.push_back(sub_item.second.get_value<string>());
        }
    }
    catch (...) {
        log("error occurred while parsing json"); //TODO: send message to gs
        return vector<string>();
    }

    return ret;
}

string Util::parse_json_value(initializer_list<string> args) {
    pt::ptree root;
    pt::read_json("../src/config.json", root);
    string path = "";
    string ret = "";

    if(args.size() == 0) {
        log("error: no arguments to parse json"); //TODO: send message to gs
        return "";
    }

    try {
        for (string s : args) {
            path += s + ".";
        }
        ret = root.get<string>(path.substr(0, path.length() - 1));
    }
    catch (...) {
        log("error occurred while parsing json"); //TODO: send message to gs
        return "";
    }

    return ret;
}

string Util::map_to_string(map<string, string> data, string key_delim, string element_delim){
    string output = "";
    map<string, string>::iterator it = data.begin();
    while(it != data.end()){
        string key = it->first;
        string value = it->second;
        output += key + key_delim + value;
        output += element_delim;
        it++;
    }
    return output;
}


map<string, string> Util::string_to_map(string data, string key_delim, string element_delim){
    map<string, string> output;
    string temp = data;

    size_t pos;
    while((pos = temp.find(element_delim)) != string::npos){
        string token = temp.substr(0, pos);
        size_t split = token.find(key_delim);
        assert(split != string::npos);
        string key = token.substr(0, split);
        token.erase(0, split + key_delim.length());
        output.insert(pair<string, string>(key, token));
        temp.erase(0, pos + element_delim.length());
    }

    return output;
}

void Util::enqueue(Flag *flag, Log log, LogPriority logPriority) {
    Packet packet = Packet(logPriority);
    packet.add(log);
    auto queue = flag->get<priority_queue<Packet, vector<Packet>, Packet::compareTo>>("telemetry.enqueue");
    queue.push(packet);
    flag->put("telemetry.enqueue", queue);
}