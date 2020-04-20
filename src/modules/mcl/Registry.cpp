#include <queue>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Field.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>

namespace pt = boost::property_tree;

Registry::Registry(){
    log("Registry created");

    //parsing from json: https://www.codespeedy.com/read-data-from-json-file-in-cpp/

    pt::ptree root;
    pt::read_json("flight/modules/lib/config.json", root);

    // Sensor fields
    auto sensor = root.get_child("sensors").get_child("list");
    for(auto &outer : sensor) {
        for(auto &inner : sensor.get_child(outer.first)) {
            add<double>("sensor_measured." + outer.first + "." + inner.second.get_value<std::string>(), 0.0);
            add<double>("sensor_normalized." + outer.first + "." + inner.second.get_value<std::string>(), 0.0);
            add<SensorStatus>("sensor_status." + outer.first + "." + inner.second.get_value<std::string>(), SensorStatus::SAFE);
        }
    }

    // Valve fields
    auto valve = root.get_child("valves").get_child("list");
    for(auto &outer : sensor) {
        for(auto &inner : sensor.get_child(outer.first)) {
            add<SolenoidState>("valve." + outer.first + "." + inner.second.get_value<std::string>(), SolenoidState::CLOSED);
            add<ActuationType>("valve_actuation." + outer.first + "." + inner.second.get_value<std::string>(), ActuationType::NONE);
        }
    }

    // Telemetry fields
    add<priority_queue<int>>("telemetry.ingest_queue");
    add<bool>("telemetry.status", false);
    add<bool>("telemetry.resetting", false);

    // General fields
    add<bool>("general.hard_abort", false);
    add<bool>("general.soft_abort", false);
    add<Stage>("general.stage", Stage::PROPELLANT_LOADING);
    add<int>("general.stage_progress", 0);
}

