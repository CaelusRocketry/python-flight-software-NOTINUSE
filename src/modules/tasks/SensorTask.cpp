#include <assert.h>
#include <Logger/logger_util.h>
#include <flight/modules/tasks/SensorTask.hpp>

void SensorTask::initialize(){
    log("Sensor task is initialized");
}


void SensorTask::read(){
    log("Reading from sensors");
}

void SensorTask::actuate(){
    log("Actuating sensors");
}