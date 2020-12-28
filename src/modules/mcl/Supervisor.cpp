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

Supervisor::~Supervisor() {
    delete control_task;

    for (auto task : tasks) {
        delete task;
    }
}

void Supervisor::initialize() {
    /* Load config */
    ifstream config_file("../config.json");
    json j = json::parse(config_file);
    global_config = Config(j);
    global_registry.initialize();

    log("Supervisor: Parsing config");
    parse_config();

    log("Tasks: Initializing");
    for (Task* task : tasks){
        task->initialize();
    }

    log("Control tasks: Initializing");
    control_task->begin();
}

void Supervisor::read() {
    log("Supervisor: Reading");
    for (Task* task : tasks){
        task->read();
    }
}

void Supervisor::control() {
    log("Supervisor: Controlling");

    control_task->control();
}

void Supervisor::actuate() {
    log("Supervisor: Actuating");
    for (Task* task : tasks){
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

void Supervisor::parse_config() {
    // parse_json_list automatically parses config.json
    for (const string& task : global_config.task_config.tasks) {
        if (task == "sensor") tasks.push_back(new SensorTask());
        if (task == "telemetry") tasks.push_back(new TelemetryTask());
        if (task == "valve") tasks.push_back(new ValveTask());
    }

    set<string> control_tasks;
    for (const string& control_task : global_config.task_config.control_tasks) {
        control_tasks.insert(control_task);
        log("Control task [" + control_task + "]: Enabled");
    }

    control_task = new ControlTask(control_tasks);
}