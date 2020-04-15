#include <thread> // For time delay
#include <Logger/logger_util.h>
#include <flight/modules/mcl/Supervisor.hpp>

Supervisor::Supervisor(){
    log("Running the constructor");
    this->name = "Supervisor";
    this->registry = new Registry();
    this->flag = new Flag();
    log(this->name);
}

void Supervisor::initialize(){
    log("Initializing");
}

void Supervisor::read(){
    log("Reading");
}

void Supervisor::control(){
    log("Controlling");
}

void Supervisor::actuate(){
    log("Actuating");
}

void Supervisor::run(){
    while(true){
        read();
        control();
        actuate();
        this_thread::sleep_for(chrono::seconds(1));
    }
}