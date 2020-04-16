#include <assert.h>
#include <Logger/logger_util.h>
#include <flight/modules/tasks/TelemetryTask.hpp>

TelemetryTask::TelemetryTask(Registry* registry, Flag* flag){
    this->_registry = registry;
    this->_flag = flag;
    _telemetry = new Telemetry();
    log("Telemetry task created");
}


void TelemetryTask::read(){
    _telemetry->run("ws://127.0.0.1:9002");
    int val = _registry->get<int>("general.stage_progress");
    log(to_string(val));
}

void TelemetryTask::actuate(){
    int val = _registry->get<int>("general.stage_progress");
    bool worked = _registry->put<int>("general.stage_progress", val + 1);
    assert(worked);
}