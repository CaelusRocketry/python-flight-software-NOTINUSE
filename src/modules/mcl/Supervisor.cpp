#include <thread> // For time delay
#include <Logger/logger_util.h>
#include <flight/modules/mcl/Supervisor.hpp>
#include <flight/modules/tasks/SensorTask.hpp>
#include <flight/modules/tasks/TelemetryTask.hpp>
#include <flight/modules/tasks/ValveTask.hpp>
#include <flight/modules/lib/Util.hpp>

//TODO: wrap everything in a try catch to make sure that execution doesn't stop if/when an error gets thrown?

Supervisor::Supervisor(){
    log("Creating registry and flag");
    registry = new Registry();
    flag = new Flag();

    log("Creating tasks");
    auto config = parse_config();

    log("Creating control tasks");
    controlTask = new ControlTask(registry, flag, config);
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
        this_thread::sleep_for(chrono::seconds(1)); // temp placeholder for TimerControl
    }
}

unordered_map<string, bool> Supervisor::parse_config() {
    // parse_json_list automatically parses config.json
    auto task_config = Util::parse_json_list({"task_config", "tasks"});
    auto control_task_config = Util::parse_json_list({"task_config", "control_tasks"});

    // unordered dict essentially
    unordered_map<string, bool> control_tasks;

    for(string task : task_config) {
        if(task.compare("sensor") == 0) {
            tasks.push_back(new SensorTask(registry, flag));
        }
        if(task.compare("telemetry") == 0) {
            tasks.push_back(new TelemetryTask(registry, flag));
        }
        if(task.compare("valve") == 0) {
            tasks.push_back(new ValveTask(registry, flag));
        }
    }

    for(string control_task : control_task_config) {
        control_tasks[control_task] = true;
    }

    return control_tasks;
}