#include <thread> // For time delay
#include <Logger/logger_util.h>
#include <flight/modules/mcl/Supervisor.hpp>

Supervisor::Supervisor(){
    log("Running the constructor");
    name = "Supervisor";
    registry = new Registry();
    flag = new Flag();
    log(name);
}

void Supervisor::initialize(){
    log("Initializing");
}

void Supervisor::read(){
    registry->put<int>("general.stage_progress", 0);
//    registry->put<int>("general.stage_progress", 0);
//    int val = registry->get<int>("general.stage_progress");
//    int val = registry->get<int>("general.stage_progress");
//    log("Current value: " + to_string(val));
}

void Supervisor::control(){
//    log("Controlling");
}

void Supervisor::actuate(){
//    int val = registry->get<int>("general.stage_progress");
//    bool worked = registry->put<int>("general.stage_progress", val + 1);
/*
    bool worked = false;
    if(worked){
        log("Put was successful");
    }
    else{
        log("Put was unsuccessful");
    }
    */
}

void Supervisor::run(){
    while(true){
        read();
        control();
        actuate();
        this_thread::sleep_for(chrono::seconds(1));
    }
}