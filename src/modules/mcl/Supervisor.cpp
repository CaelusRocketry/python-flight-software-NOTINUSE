#include <thread> // For time delay
#include <assert.h>
#include <Logger/logger_util.h>
#include <flight/modules/mcl/Supervisor.hpp>

Supervisor::Supervisor(){
    log("Running the constructor");
    name = "Supervisor";
    registry = new Registry();
    flag = new Flag();
    task = new TelemetryTask();
    log(name);
}

void Supervisor::initialize(){
    log("Initializing");
}

void Supervisor::read(){
    int val = registry->get<int>("general.stage_progress");
    log(to_string(val));
}

void Supervisor::control(){
    log("Controlling");
}

void Supervisor::actuate(){
    int val = registry->get<int>("general.stage_progress");
    bool worked = registry->put<int>("general.stage_progress", val + 1);
    assert(worked);
}

void Supervisor::run(){
    while(true){
        read();
        control();
        actuate();
        this_thread::sleep_for(chrono::seconds(1));
    }
}