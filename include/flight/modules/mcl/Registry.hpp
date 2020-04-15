#ifndef FLIGHT_REGISTRY_HPP
#define FLIGHT_REGISTRY_HPP

#include <string>
using namespace std;

class Registry {
private:

public:
    Registry();
    void get(string name);
    void put(string name);
};

#endif //FLIGHT_REGISTRY_HPP

