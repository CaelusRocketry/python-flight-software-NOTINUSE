#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <flight/modules/mcl/Config.hpp>
#include <Logger/logger_util.h>

void Registry::initialize() {
    log("Registry: Initializing");

    log("Registry: Reading Sensors List");
    // Sensor fields
    for (const auto& type_pair : global_config.sensors.list) {
        string type = type_pair.first;
        for (const auto& location_ : type_pair.second) {
            string location = location_.first;
            auto &sensor = sensors[type][location];
            sensor.measured_value = 0.0;
            sensor.normalized_value = 0.0;
            sensor.status = SensorStatus::SAFE;
        }
    }

    log("Registry: Reading Valves List");
    // Valve fields
    for (const auto& type_pair : global_config.valves.list) { // [solenoid]
        string type = type_pair.first;
        for (const auto &location_ : type_pair.second) { // ["pressure_relief", "propellant_vent", "main_propellant_valve"]
            string location = location_.first;
            auto &valve = valves[type][location];
            valve.state = SolenoidState::CLOSED;
            valve.actuation_type = ActuationType::NONE;
            valve.actuation_priority = ValvePriority::NONE;
        }
    }

    log("Registry: Setting default values for telemetry and general fields");
    // Telemetry fields
    telemetry.status = false;
    telemetry.resetting = false;

    // General fields
    general.hard_abort = false;
    general.soft_abort = false;
    general.stage = Stage::WAITING;
    general.stage_status = 0.0;
    general.stage_progress = 0;
}

bool Registry::valve_exists(const string& type, const string& location) {
    return (valves.count(type) > 0) && (valves.at(type).count(location) > 0);
}

bool Registry::sensor_exists(const string &type, const string &location) {
    return (sensors.count(type) > 0) && (sensors.at(type).count(location) > 0);
}

// Define the value declared with extern in the header file
Registry global_registry;
