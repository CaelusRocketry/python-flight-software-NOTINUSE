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
//    tasks.push_back(new SensorTask(registry, flag));
    tasks.push_back(new ValveTask(registry, flag));

    log("Creating control tasks");
    controlTask = new ControlTask(registry, flag, {{"sensor", false}, {"telemetry", false}, {"valve", false}, {"stage", false}});
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
    for(Task* task : tasks){
        task->read();
    }
}

void Supervisor::control(){
    controlTask->control();
}

void Supervisor::actuate(){
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