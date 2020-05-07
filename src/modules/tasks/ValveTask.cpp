#include <bitset>
#include <assert.h>
#include <Logger/logger_util.h>
#include <flight/modules/tasks/ValveTask.hpp>
#include <flight/modules/lib/Util.hpp>

void ValveTask::initialize(){
    log("Valve task started");
    valve_list.push_back(make_tuple("solenoid", "main_propellant_valve"));
    valve_list.push_back(make_tuple("solenoid", "pressure_relief"));
    valve_list.push_back(make_tuple("solenoid", "propellant_vent"));

    valve = new Arduino("PseudoValve");
}


void ValveTask::read(){
    log("Reading");
    char* data = valve->read();

    uint32_t int_data;
    memcpy(&int_data, data, sizeof(int));
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
    this->actuate_solenoids();
}

void ValveTask::actuate_solenoids() {
    auto locations = Util::parse_json_list({"valves", "list", "solenoid"});
    for(int loc_idx = 0; loc_idx < locations.size(); loc_idx++) {
        auto loc = locations[loc_idx];
        auto actuation_type = this->flag->get<ActuationType>("valve_actuation_type.solenoid." + loc);
        auto actuation_priority = this->flag->get<ValvePriority>("valve_actuation_priority.solenoid." + loc);

        if(actuation_priority != ValvePriority::NONE) {
            auto current_priority = this->registry->get<ValvePriority>("valve_actuation_priority.solenoid." + loc);
            char ret[2];
            ret[0] = loc_idx;

            if(int(actuation_priority) >= int(current_priority)) {
                if(actuation_type == ActuationType::NONE) {
                    log("Allowing others to actuate"); //TODO: change to enqueue
                    ret[1] = int(ActuationType::NONE);
                    this->registry->put("valve_actuation_type.solenoid." + loc, actuation_type);
                    this->registry->put("valve_actuation_priority.solenoid." + loc, ValvePriority::NONE);
                }
                else {
                    ret[1] = int(actuation_type);
                    log("Actuating..."); //TODO: change to enqueue
                    this->registry->put("valve_actuation_type.solenoid." + loc, actuation_type);
                    this->registry->put("valve_actuation_priority.solenoid." + loc, actuation_priority);
                }

                this->valve->write(ret);
                this->registry->put("valve_actuation_type.solenoid." + loc, ActuationType::NONE);
                this->registry->put("valve_actuation_priority.solenoid." + loc, ValvePriority::NONE);
            }
        }
    }
}