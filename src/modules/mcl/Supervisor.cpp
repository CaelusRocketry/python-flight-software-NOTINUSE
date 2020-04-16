#include <thread> // For time delay
#include <Logger/logger_util.h>
#include <flight/modules/mcl/Supervisor.hpp>

Supervisor::Supervisor(){
    log("Running the constructor");
    name = "Supervisor";
    registry = new Registry();
    flag = new Flag();
    task = new TelemetryTask(registry, flag);
    log(name);
}

void Supervisor::initialize(){
    log("Initializing");
}

void Supervisor::read(){
    task->read();
}

void Supervisor::control(){
    log("Controlling");
}

void Supervisor::actuate(){
    task->actuate();
}

void Supervisor::run(){
    while(true){
        read();
        control();
        actuate();
        this_thread::sleep_for(chrono::seconds(1));
    }
}