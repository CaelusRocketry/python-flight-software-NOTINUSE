#include <queue>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Field.hpp>

Registry::Registry(){
    log("Registry created");

    //TODO: convert this to parsing from json: https://www.codespeedy.com/read-data-from-json-file-in-cpp/

    // Sensor fields
    add<double>("sensor_measured.thermocouple.chamber", 0.0);
    add<double>("sensor_measured.thermocouple.tank", 0.0);
    add<double>("sensor_measured.pressure.chamber", 0.0);
    add<double>("sensor_measured.pressure.tank", 0.0);
    add<double>("sensor_measured.pressure.injector", 0.0);
    add<double>("sensor_measured.load.tank", 0.0);

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

