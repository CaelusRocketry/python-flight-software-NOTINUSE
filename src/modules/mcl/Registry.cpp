#include <queue>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Field.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <flight/modules/lib/Util.hpp>

Registry::Registry(){
    log("Registry created");

    // Sensor fields
    for(string outer : Util::parse_json({"sensors", "list"})) {
        for(string inner : Util::parse_json_list({"sensors", "list", outer})) {
            add<double>("sensor_measured." + outer + "." + inner, 0.0);
            add<double>("sensor_normalized." + outer + "." + inner, 0.0);
            add<SensorStatus>("sensor_status." + outer + "." + inner, SensorStatus::SAFE);

        }
    }

    // Valve fields
    for(string outer : Util::parse_json({"valves", "list"})) {
        for(string inner : Util::parse_json_list({"valves", "list", outer})) {
            add<SolenoidState>("valve." + outer + "." + inner, SolenoidState::CLOSED);
            add<ActuationType>("valve_actuation." + outer + "." + inner, ActuationType::NONE);
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

