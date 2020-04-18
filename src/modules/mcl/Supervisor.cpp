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
//    tasks.push_back(new TelemetryTask(registry, flag));
//    tasks.push_back(new ValveTask(registry, flag));
}

void Supervisor::initialize(){
    log("Initializing tasks");
    for(Task* task : tasks){
        task->initialize();
    }
}

void Supervisor::read(){
    log("Reading from tasks");
    for(Task* task : tasks){
        task->read();
    }
}

void Supervisor::control(){
//    log("Sensor value: " + to_string(registry->get<double>("sensor_measured.thermocouple.chamber")));
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