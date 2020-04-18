#include <thread>
#include <chrono>
#include <Logger/logger_util.h>
#include <flight/modules/drivers/PseudoValve.hpp>

PseudoValve::PseudoValve(){
    // List all solenoids (this should normally be done in a config.json)
    solenoid_locs.push_back("main_propellant_valve");
    solenoid_locs.push_back("pressure_relief");
    solenoid_locs.push_back("propellant_vent");
    num_solenoids = solenoid_locs.size();
    // Initialize valve states to be closed and actuations to be none
    for(auto valve : solenoid_locs){
        valve_states[make_tuple("solenoid", valve)] = "closed";
        valve_actuations[make_tuple("solenoid", valve)] = "none";
    }
}

char* PseudoValve::read(){
    union Conversion {
        uint32_t value;
        char bytes[4];
    };
    uint32_t data;
    for(int i = 0; i < num_solenoids; i++){
        string actuation = valve_actuations[make_tuple("solenoid", solenoid_locs[i])];
        int state = actuation_dict.at(actuation);
        data = data | (state << (i * 2 + 1));
    }
    Conversion conv;
    conv.value = data;
    return conv.bytes;
}

// Timer in milliseconds
void PseudoValve::actuate(tuple<string, string> valve, string state1, double timer, string state2){
    valve_states[valve] = state1;
    if(timer != -1){
        this_thread::sleep_for(chrono::milliseconds((long)(timer * 1000)));
    }
    valve_states[valve] = state2;
    log("Finished actuating: " + get<0>(valve));
    if(timer != -1){
        log("Setting valve actuation type to NONE");
        valve_actuations[valve] = "none";
    }
}

void PseudoValve::write(char* msg){
    auto loc_idx = msg[0];
    auto actuation_idx = msg[1];
    auto valve = make_tuple("solenoid", solenoid_locs[loc_idx]);
    auto actuation_type = inv_actuation_dict.at(actuation_idx);

    string state1;
    double timer;
    string state2;

    switch(actuation_dict.at(actuation_type)){
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
//    thread act(&PseudoValve::actuate, valve, state1, timer, state2);
//    act.detach();
}