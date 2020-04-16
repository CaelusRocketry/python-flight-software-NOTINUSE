#include <queue>
#include <Logger/logger_util.h>
#include <flight/modules/tasks/TelemetryTask.hpp>

TelemetryTask::TelemetryTask(){
    telemetry = new Telemetry();
    log("Telemetry task created");
}

void TelemetryTask::read(){
    log("Reading");
}

void TelemetryTask::actuate(){
    log("Actuating");
}