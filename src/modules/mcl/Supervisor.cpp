#include <thread> // For time delay
#include <set>
#include <Logger/logger_util.h>
#include <flight/modules/mcl/Supervisor.hpp>
#include <flight/modules/tasks/SensorTask.hpp>
#include <flight/modules/tasks/TelemetryTask.hpp>
#include <flight/modules/tasks/ValveTask.hpp>
#include <flight/modules/lib/Util.hpp>
#include <flight/modules/mcl/Config.hpp>

using json = nlohmann::json;

//TODO: wrap everything in a try catch to make sure that execution doesn't stop if/when an error gets thrown?

Supervisor::Supervisor(){
    log("Creating registry and flag");
    registry = new Registry();
    flag = new Flag();

    log("Creating tasks");
    log("Creating control tasks");
    controlTask = new ControlTask(parse_config());
}

Supervisor::~Supervisor() {
    delete registry;
    delete flag;
    delete controlTask;

    for(auto task : tasks) {
        delete task;
    }
}

void Supervisor::initialize() {
    /* Load config */
    ifstream config_file("../../config.json");
    json j = json::parse(config_file);
    global_config = Config(j);

    log("Initializing tasks");
    for(Task* task : tasks){
        task->initialize();
    }

    log("Initializing control tasks");
    controlTask->begin();
}

void Supervisor::read(){
    log("Reading...");
    for(Task* task : tasks){
        task->read();
    }
}

void Supervisor::control(){
    log("Controlling...");
    controlTask->control();
}

void Supervisor::actuate(){
    log("Actuating...");
    for(Task* task : tasks){
        task->actuate();
    }
}

void Supervisor::run() {
    while (true) {
        read();
        control();
        actuate();
        this_thread::sleep_for(chrono::seconds(1)); // temp placeholder for TimerControl
    }
}

set<string> Supervisor::parse_config() {
    // parse_json_list automatically parses config.json
    auto task_config = Util::parse_json_list({"task_config", "tasks"});
    auto control_task_config = Util::parse_json_list({"task_config", "control_tasks"});

    // unordered dict essentially
    set<string> control_tasks;

    for (const string& task : task_config) {
        if (task == "sensor") tasks.push_back(new SensorTask());
        if (task == "telemetry") tasks.push_back(new TelemetryTask());
        if (task == "valve") tasks.push_back(new ValveTask());
    }

    for (const string& control_task : control_task_config) {
        control_tasks.insert(control_task);
    }

    return control_tasks;
}