#include <queue>
#include "flight/modules/mcl/Flag.hpp"
#include <Logger/logger_util.h>
#include <flight/modules/lib/Enums.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>

namespace pt = boost::property_tree;

Flag::Flag(){
    log("Flag created");
    //parsing from json: https://www.codespeedy.com/read-data-from-json-file-in-cpp/

    pt::ptree root;
    pt::read_json("../src/config.json", root);

    //general fields
    add<bool>("general.progress", false);

    //telemetry fields
    add<priority_queue<int>>("telemetry.enqueue");
    add<priority_queue<int>>("telemetry.send_queue");
    add<bool>("telemetry.reset", true);

    //solenoid fields
    auto sensor = root.get_child("sensors").get_child("list");
    for(auto &location : sensor) {
        add<ActuationType>("solenoid.actuation_type." + location.first, ActuationType::NONE);
        add<ValvePriority>("solenoid.actuation_priority." + location.first, ValvePriority::NONE);
    }
}