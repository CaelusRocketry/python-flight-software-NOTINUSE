#include <assert.h>
#include <Logger/logger_util.h>
#include <flight/modules/tasks/ValveTask.hpp>

void ValveTask::initialize(){
    log("Valve task is initialized");
}


void ValveTask::read(){
    log("Reading from valves");
}

void ValveTask::actuate(){
    log("Actuating valves");
}