//
// Created by adiv413 on 4/27/2020.
//

#include <flight/modules/lib/Util.hpp>

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