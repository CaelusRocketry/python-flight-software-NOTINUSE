#include <bitset>
#include <assert.h>
#include <Logger/logger_util.h>
#include <flight/modules/tasks/ValveTask.hpp>

void ValveTask::initialize(){
    valve_list.push_back(make_tuple("solenoid", "main_propellant_valve"));
    valve_list.push_back(make_tuple("solenoid", "pressure_relief"));
    valve_list.push_back(make_tuple("solenoid", "propellant_vent"));

    valve = new Arduino("PseudoValve");
}


void ValveTask::read(){
    log("Reading");
    union Conversion {
        uint32_t value;
        char bytes[4];
    };
    char* data = valve->read();
    Conversion conv;
    for(int i = 0; i < 4; i++){
        conv.bytes[i] = data[i];
    }
    uint32_t int_data = conv.value;
    constexpr int num_bits = NUM_VALVES * 2 + 1;
    string str_data = bitset<num_bits>(int_data).to_string();
    vector<ActuationType> actuations;
    log("Getting actuations");
    log("int_data is: " + to_string(int_data));
    log("str_data is: " + str_data);
    for(int i = 0; i < NUM_VALVES; i++){
        string sub = str_data.substr(num_bits - (i+1)*2 - 1, num_bits - i*2 - 1);
        int actuation_int = stoi(sub);
        actuations.push_back(static_cast<ActuationType>(actuation_int));
    }

    for(int i = 0; i < NUM_VALVES; i++){
        auto path = valve_list[i];
        string type = get<0>(path);
        string loc = get<1>(path);
        registry->put<ActuationType>("valve_actuation_type." + type + "." + loc, actuations[i]);
        if(actuations[i] == ActuationType::NONE || actuations[i] == ActuationType::CLOSE_VENT) {
            registry->put<SolenoidState>("valve." + type + "." + loc, SolenoidState::CLOSED);
            log("CLOSED");
        }
        else{
            log("OPEN");
            registry->put<SolenoidState>("valve." + type + "." + loc, SolenoidState::OPEN);
        }
    }
}


void ValveTask::actuate(){
    log("Actuating valves");
}