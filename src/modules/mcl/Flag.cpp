#include <queue>
#include "flight/modules/mcl/Flag.hpp"
#include <Logger/logger_util.h>

Flag::Flag(){
    log("Flag created");
    //TODO: convert this to parsing from json: https://www.codespeedy.com/read-data-from-json-file-in-cpp/

    //general fields
    add<bool>("general.progress", false);

    //telemetry fields
    add<priority_queue<int>>("telemetry.enqueue");
    add<priority_queue<int>>("telemetry.send_queue");
    add<bool>("telemetry.reset", true);

    //solenoid fields
    //TODO: add this once the enums are done
}