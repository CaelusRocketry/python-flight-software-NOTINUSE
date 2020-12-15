#include <queue>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Field.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <flight/modules/lib/Util.hpp>
#include <flight/modules/lib/Packet.hpp>

// Adds all registry fields from config and general default fields

Registry::Registry() {
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
    for(string outer : Util::parse_json({"valves", "list"})) {  // [solenoid]
        for(string inner : Util::parse_json_list({"valves", "list", outer})) {  // ["pressure_relief", "propellant_vent", "main_propellant_valve"]
            add<SolenoidState>("valve." + outer + "." + inner, SolenoidState::CLOSED);
            add<ActuationType>("valve_actuation_type." + outer + "." + inner, ActuationType::NONE);
            add<ValvePriority>("valve_actuation_priority." + outer + "." + inner, ValvePriority::NONE);
        }
    }

    // Telemetry fields
    add<priority_queue<Packet, vector<Packet>, Packet::compareTo>>("telemetry.ingest_queue");
    add<bool>("telemetry.status", false);
    add<bool>("telemetry.resetting", false);

    // General fields
    add<bool>("general.hard_abort", false);
    add<bool>("general.soft_abort", false);
    add<Stage>("general.stage", Stage::WAITING);
    add<double>("general.stage_status", 0.0);
    add<int>("general.stage_progress", 0);
}

