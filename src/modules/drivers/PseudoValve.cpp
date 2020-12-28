#include <thread>
#include <chrono>
#include <Logger/logger_util.h>
#include <flight/modules/drivers/PseudoValve.hpp>
#include <flight/modules/mcl/Config.hpp>
#include <flight/modules/mcl/Registry.hpp>

// Extends PseudoArduino
PseudoValve::PseudoValve(){
    /* Pair<Location, Config> */
    for (auto pair : global_config.valves.list["solenoid"]) {
        solenoid_locs.push_back(pair.first);
    }

    num_solenoids = solenoid_locs.size();

    // Initialize valve states to be closed and actuations to be none
    for (auto valve : solenoid_locs){
        valve_states[{"solenoid", valve}] = "closed";
        valve_actuations[{"solenoid", valve}] = "none";
    }
}

/*
 * Convert human-readable actuation data to unreadable bytes data to simulate what we'd get from an Arduino
 */
unsigned char* PseudoValve::read() {
    unsigned char *data = new unsigned char[num_solenoids * 3];

    // pin, state, actuation_type
    for (int i = 0; i < solenoid_locs.size(); i++) {
        unsigned char solenoid_data[3];
        RegistryValveInfo solenoid = global_registry.valves["solenoid"][solenoid_locs[i]];
        int pin = global_config.valves.list["solenoid"][solenoid_locs[i]].pin;

        solenoid_data[0] = pin;
        solenoid_data[1] = (unsigned char) solenoid.state;
        solenoid_data[2] = (unsigned char) solenoid.actuation_type;

        data[i * 3 + 0] = solenoid_data[0];
        data[i * 3 + 1] = solenoid_data[1];
        data[i * 3 + 2] = solenoid_data[2];
    }

    return data;
}

// Timer in milliseconds
void PseudoValve::actuate(const pair<string, string>& valve, const string& state1, double timer, const string& state2){
    valve_states[valve] = state1;
    if (timer != -1) {
        this_thread::sleep_for(chrono::milliseconds((long)(timer * 1000)));
    }
    valve_states[valve] = state2;
    log("Finished actuating: " + valve.first + "." + valve.second);
    if (timer != -1) {
        log("Setting valve actuation type to NONE");
        valve_actuations[valve] = "none";
    }
}

void PseudoValve::write(unsigned char* msg) {
    auto loc_idx = msg[0];
    auto actuation_idx = msg[1];
    pair<string, string> valve {"solenoid", solenoid_locs[loc_idx]};
    auto actuation_type = inv_actuation_dict.at(actuation_idx);

    string state1;
    double timer;
    string state2;

    switch(actuation_dict.at(actuation_type)) {
        case 2:
            state1 = "open";
            timer = -1;
            state2 = "open";
            break;
        case 0:
        case 1:
            state1 = "closed";
            timer = -1;
            state2 = "closed";
            break;
        case 3:
            state1 = "open";
            timer = 2.0;
            state2 = "closed";
            break;
        default:
            break;
    }
    valve_actuations[valve] = actuation_type;
    thread act([=] { actuate(valve, state1, timer, state2); });
    act.detach();
}