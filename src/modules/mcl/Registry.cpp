#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <flight/modules/mcl/Config.hpp>

// Adds all registry fields from config and general default fields

Registry::Registry() {}

void Registry::initialize() {
    log("Registry: Initializing");

    log("Registry: Reading Sensors List");
    // Sensor fields
    for (const auto& type_ : global_config.sensors.list) {
        string type = type_.first;
        auto locations = type_.second;
        for (const auto& location_ : locations) {
            string location = location_.first;
            auto &sensor = sensors[type][location];
            sensor.measured_value = 0.0;
            sensor.normalized_value = 0.0;
            sensor.status = SensorStatus::SAFE;
        }
    }

    log("Registry: Reading Valves List");
    // Valve fields
    for (const auto& type_ : global_config.valves.list) { // [solenoid]
        string type = type_.first;
        auto locations = type_.second;
        for (const auto &location_ : locations) { // ["pressure_relief", "propellant_vent", "main_propellant_valve"]
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

// Define the value declared with extern in the header file
Registry global_registry;
