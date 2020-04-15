#include <iostream>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>

#ifndef FLIGHT_SUPERVISOR_HPP
#define FLIGHT_SUPERVISOR_HPP

using namespace std;

class Supervisor {
    private:
        string name;
        Registry* registry;
        Flag* flag;

    public:
        Supervisor();
        void initialize();
        void read();
        void control();
        void actuate();
        void run();
};

#endif //FLIGHT_SUPERVISOR_HPP