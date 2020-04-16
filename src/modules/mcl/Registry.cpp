#include <queue>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Field.hpp>

Registry::Registry(){
    log("Registry created");

    // Sensor fields

    // Valve fields

    // Telemetry fields
    add<priority_queue<int>>("telemetry.ingest_queue");
    add<bool>("telemetry.status", false);
    add<bool>("telemetry.resetting", false);

    // General fields
    add<bool>("general.hard_abort", false);
    add<bool>("general.soft_abort", false);
    add<int>("general.stage", 0);
    add<int>("general.stage_progress", 0);
}

