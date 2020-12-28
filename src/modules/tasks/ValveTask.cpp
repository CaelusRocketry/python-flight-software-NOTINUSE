#include <Logger/logger_util.h>
#include <flight/modules/tasks/ValveTask.hpp>
#include <flight/modules/lib/Util.hpp>
#include <flight/modules/mcl/Config.hpp>

const unsigned char SEND_DATA_CMD = 255;
const unsigned char ACTUATE_CMD = 254;

void ValveTask::initialize() {
    log("Valve task: Starting");
    for (const auto& valve_type : global_config.valves.list) {
        string type = valve_type.first;
        auto valve_locations = valve_type.second;
        for (const auto& valve_location : valve_locations) {
            string location = valve_location.first;
            ConfigValveInfo valve_info = valve_location.second;
            int pin = valve_info.pin;

            pin_to_valve[pin].first = type;
            pin_to_valve[pin].second = location;

            valve_list.push_back(make_pair(type, location));
        }
    }
    arduino = new Arduino("PseudoValve");
}

void ValveTask::begin() {
    this->send_valve_info();
}

void ValveTask::send_valve_info() {
    unsigned char *buf = new unsigned char[1 + NUM_VALVES * 3];

    buf[0] = NUM_VALVES;
    for (int i = 0; i < NUM_VALVES; i++) {
        auto valve_ = valve_list[i];

        string type = valve_.first;
        string location = valve_.second;

        // Send pin<int>, is valve special<bool>, and the natural state of the valve<SolenoidState; represented as a string>.
        ConfigValveInfo valve = global_config.valves.list[type][location];

        buf[i * 3 + 0] = valve.pin;
        buf[i * 3 + 1] = valve.special;
        buf[i * 3 + 2] = valve.natural_state == "OPEN" ? 1 : 0;
    }

    arduino->write(buf);

    // TODO add confirmation check here
}

/*
 * Reads all actuation states from valve and updates registry
 *
 * Reads data from valve as char*, converts each data to an ActuationType and updates the registry from there.
 */
void ValveTask::read(){
    log("Valve: Reading");

//    arduino->write(new unsigned char[1] {SEND_DATA_CMD});
    unsigned char* data = arduino->read();

    for (int i = 0; i < NUM_VALVES; i++){
        unsigned char solenoid_data[3];
        solenoid_data[0] = data[i * 3];
        solenoid_data[1] = data[i * 3 + 1];
        solenoid_data[2] = data[i * 3 + 2];

        int pin = solenoid_data[0];
        auto state = static_cast<SolenoidState>(solenoid_data[1]);
        auto actuation_type = static_cast<ActuationType>(solenoid_data[2]);

        string valve_type = pin_to_valve[pin].first;
        string valve_location = pin_to_valve[pin].second;

        /* Update the registry */
        global_registry.valves[valve_type][valve_location].state = state;
        global_registry.valves[valve_type][valve_location].actuation_type = actuation_type;
    }
}


void ValveTask::actuate(){
    log("Actuating valves");
    actuate_solenoids();
}

/*
 * For each solenoid:
 *  if the actuation priority attached to that solenoid is not NONE and is greater than the current priority:
 *      allow the solenoid to be actuated
 *  else:
 *      deny the request to actuate this solenoid, revert back to the current actuation
 */

void ValveTask::actuate_solenoids() {
    for (const auto& valve_ : valve_list) {
        string valve_type = valve_.first;
        string valve_location = valve_.second;

        if (valve_type != "solenoid") {
            continue;
        }

        int pin = global_config.valves.list[valve_type][valve_location].pin;
        FlagValveInfo target_valve_info = global_flag.valves[valve_type][valve_location];
        RegistryValveInfo current_valve_info = global_registry.valves[valve_type][valve_location];

        if (
            target_valve_info.actuation_priority != ValvePriority::NONE &&
            target_valve_info.actuation_priority >= current_valve_info.actuation_priority
        ) {
            /* Update the registry */
            global_registry.valves[valve_type][valve_location].actuation_type = target_valve_info.actuation_type;
            global_registry.valves[valve_type][valve_location].actuation_priority = target_valve_info.actuation_priority;

            /* Send command to actuate */
            unsigned char command[3];
            command[0] = ACTUATE_CMD;
            command[1] = pin;
            command[2] = static_cast<char>(target_valve_info.actuation_type);

            arduino -> write(command);

            /* Reset the flags */
            global_flag.valves[valve_type][valve_location].actuation_type = ActuationType::NONE;
            global_flag.valves[valve_type][valve_location].actuation_priority = ValvePriority::NONE;

            global_flag.log_info("response", {
                {"header", "info"},
                {"Description", "Set actuation at " + valve_type + "." + valve_location + " to " + actuation_type_inverse_map.at(target_valve_info.actuation_type)}
            });
        } else {
            global_flag.log_info("response", {
                {"header", "info"},
                {"Description", "Allowing other valves to actuate"}
            });
        }
    }
}