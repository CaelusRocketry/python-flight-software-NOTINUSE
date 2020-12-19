#include <flight/modules/lib/Util.hpp>
#include <queue>
#include <boost/algorithm/string.hpp>

//boost is imported in Util.hpp
namespace pt = boost::property_tree;
vector<string> Util::parse_json(initializer_list<string> args) {
    pt::ptree root;
    pt::read_json("../src/config.json", root);
    auto item = root;
    vector<string> ret;

    if(args.size() == 0) {
        throw JSON_ARGUMENT_ERROR();
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
        throw JSON_PARSE_ERROR();
    }

    return ret;
}

/*
 * Example: to get a list of all the solenoids, do parse_json_list({"valves", "list", "solenoid"}).
 * Note that you have to specify the field "solenoid" in order to get the items from the list.
 */

vector<string> Util::parse_json_list(initializer_list<string> args) {
    /**
     * Returns list of things (strings) that are in the specified place in the config.json
     * To specify the place, use a list of arguments
     */

    // args is just a list of arguments
    // root is essentially a dictionary, it has key strings associated with data
    pt::ptree root;

    // stores json contents in root
    pt::read_json("../src/config.json", root);

    // convert item to auto so it can automatically adapt type.
    auto item = root;

    // it's just a more efficient list for this use case
    vector<string> ret;

    if(args.size() == 0) {
        throw JSON_ARGUMENT_ERROR();
    }

    try {
        // makes item the specified subdirectory in the json file
        for (string s : args) {
            // index into subdirectory
            item = item.get_child(s);
        }
        for (auto &sub_item : item) {
            // add items in subdirectory to list
            ret.push_back(sub_item.second.get_value<string>());
        }
    }

    // catch if the argument (args) is not in the json file.
    catch (...) {
        throw JSON_PARSE_ERROR();
    }

    return ret;
}

string Util::parse_json_value(initializer_list<string> args) {
    // root is essentially a dictionary, it has key strings associated with data
    pt::ptree root;
    pt::read_json("../src/config.json", root);
    string path = "";
    string ret = "";

    if(args.size() == 0) {
        throw JSON_ARGUMENT_ERROR();
    }

    try {
        for (string s : args) {
            path += s + ".";
        }
        ret = root.get<string>(path.substr(0, path.length() - 1));
    }
    catch (...) {
        throw JSON_PARSE_ERROR();
    }

    return ret;
}

// Return a string representation of a 1D map
string Util::map_to_string(map<string, string> data, string key_delim, string element_delim){
    string output = "{";
    map<string, string>::iterator it = data.begin();
    while(it != data.end()){
        string key = it->first;
        string value = it->second;

        // if the value is a letter, enclose it in quotes
        if(value.size() > 0 and isalpha(value[0])) {
            output += "\"" + key + "\"" + key_delim + "\"" + value + "\"";
        }
        else {
            output += "\"" + key + "\"" + key_delim + value;
        }

        output += element_delim;
        it++;
    }
    output += "}";
    return output;
}

// Converts a stringified map back to a proper map

map<string, string> Util::string_to_map(string data, string key_delim, string element_delim){
    map<string, string> output;

    // split each pair of values
    vector<string> pairs;
    boost::split(pairs, data, boost::is_any_of(element_delim));

    for(string pair_string : pairs) {
        // split into key and value
        vector<string> key_and_value;
        boost::split(key_and_value, pair_string, boost::is_any_of(key_delim));
        assert(key_and_value.size() == 2);
        output.insert(pair<string, string>(key_and_value[0], key_and_value[1]));
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