#include <assert.h>
#include <Logger/logger_util.h>
#include <flight/modules/tasks/TelemetryTask.hpp>

void TelemetryTask::initialize(){
//    _telemetry = new Telemetry();
//    _telemetry->connect();
    log("Telemetry is initialized");
}


void TelemetryTask::read(){
    log("Reading telemetry");
//    int val = _registry->get<int>("general.stage_progress");
//    log(to_string(val));
}

void TelemetryTask::actuate(){
    log("Actuating telemetry");
//    int val = _registry->get<int>("general.stage_progress");
//    bool worked = _registry->put<int>("general.stage_progress", val + 1);
//    assert(worked);
}