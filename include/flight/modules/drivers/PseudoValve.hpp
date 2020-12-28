#ifndef FLIGHT_PSEUDOVALVE_HPP
#define FLIGHT_PSEUDOVALVE_HPP

#include <vector>
#include <string>
#include <map>
#include <flight/modules/drivers/PseudoArduino.hpp>

class PseudoValve : public PseudoArduino {
private:
    int num_solenoids;
    vector<string> solenoid_locs;
    map<pair<string, string>, string> valve_states;
    map<pair<string, string>, string> valve_actuations;
    const map<string, int> state_dict = {
        {"closed", 0},
        {"open", 1}
    };
    const map<string, int> actuation_dict = {
        {"none", 0},
        {"close_vent", 1},
        {"open_vent", 2},
        {"pulse", 3}
    };
    const map<int, string> inv_actuation_dict = {
        {0, "none"},
        {1, "close_vent"},
        {2, "open_vent"},
        {3, "pulse"}
    };
    void actuate(const pair<string, string>& valve, const string& state1, double timer, const string& state2);

public:
    PseudoValve();
    unsigned char* read() override;
    void write(unsigned char* msg) override;
};

#endif //FLIGHT_PSEUDOVALVE_HPP
