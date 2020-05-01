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

    // Valve fields
    for(string outer : Util::parse_json({"valves", "list"})) {  // [solenoid]
        for(string inner : Util::parse_json_list({"valves", "list", outer})) {  // ["pressure_relief", "propellant_vent", "main_propellant_valve"]
            add<SolenoidState>("valve." + outer + "." + inner, SolenoidState::CLOSED);
            add<ActuationType>("valve_actuation_type." + outer + "." + inner, ActuationType::NONE);
            add<ValvePriority>("valve_actuation_priority." + outer + "." + inner, ValvePriority::NONE);
        }
    }
}