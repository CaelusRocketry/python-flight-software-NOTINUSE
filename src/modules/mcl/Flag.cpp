#include <queue>
#include "flight/modules/mcl/Flag.hpp"
#include <Logger/logger_util.h>
#include <flight/modules/lib/Enums.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <flight/modules/lib/Util.hpp>

Flag::Flag(){
    log("Flag created");

    //general fields
    add<bool>("general.progress", false);

    //telemetry fields
    add<priority_queue<int>>("telemetry.enqueue");
    add<priority_queue<int>>("telemetry.send_queue");
    add<bool>("telemetry.reset", true);

    //solenoid fields
    for(string s : Util::parse_json_list({"valves", "list", "solenoid"})) {
        add<ActuationType>("solenoid.actuation_type." + s, ActuationType::NONE);
        add<ValvePriority>("solenoid.actuation_priority." + s, ValvePriority::NONE);
    }
}