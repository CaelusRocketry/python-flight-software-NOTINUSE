#ifndef FLIGHT_VALVETASK_HPP
#define FLIGHT_VALVETASK_HPP

#define NUM_VALVES 3

#include <vector>
#include <flight/modules/tasks/Task.hpp>
#include <flight/modules/drivers/Arduino.hpp>
#include <flight/modules/lib/Enums.hpp>

class ValveTask : public Task {
    private:
        Arduino* arduino;
        vector<pair<string, string>> valve_list;
        string name;
        pair<string, string> pin_to_valve[14];
    public:
        ValveTask(): name("Valve Arduino") {}

        void begin();
        void send_valve_info();
        void get_command();
        void initialize();
        void read();
        void actuate();
        void actuate_solenoids();
};


#endif // FLIGHT_VALVETASK_HPP
