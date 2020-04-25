#include <thread> // For time delay
#include <Logger/logger_util.h>
#include <flight/modules/mcl/Supervisor.hpp>
#include <flight/modules/tasks/SensorTask.hpp>
#include <flight/modules/tasks/TelemetryTask.hpp>
#include <flight/modules/tasks/ValveTask.hpp>

Supervisor::Supervisor(){
    log("Creating registry and flag");
    registry = new Registry();
    flag = new Flag();

    log("Creating tasks");
    tasks.push_back(new SensorTask(registry, flag));

    log("Creating control tasks");
    controlTask = new ControlTask(registry, flag, {{"sensor", true}, {"telemetry", true}, {"valve", true}, {"stage", true}});
}

Supervisor::~Supervisor() {
    delete registry;
    delete flag;
    delete controlTask;

    for(auto task : tasks) {
        delete task;
    }
}

void Supervisor::initialize(){
    log("Initializing tasks");
    for(Task* task : tasks){
        task->initialize();
    }

    log("Initializing control tasks");
    controlTask->begin();
}

void Supervisor::read(){
    log("Reading from tasks");
    for(Task* task : tasks){
        task->read();
    }
}

void Supervisor::control(){
    log("Controlling tasks");
    controlTask->control();
}

void Supervisor::actuate(){
    log("Actuating in tasks");
    for(Task* task : tasks){
        task->actuate();
    }
}

void Supervisor::run(){
    while(true){
        read();
        control();
        actuate();
        this_thread::sleep_for(chrono::seconds(1));
    }
}