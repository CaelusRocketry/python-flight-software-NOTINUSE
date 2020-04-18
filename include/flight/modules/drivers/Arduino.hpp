#ifndef FLIGHT_ARDUINO_HPP
#define FLIGHT_ARDUINO_HPP

#include <string>
#include <flight/modules/drivers/PseudoArduino.hpp>

using namespace std;

class Arduino {
private:
    string name;
    PseudoArduino* arduino;
public:
    Arduino(string n)
    :name(n) { reset(); }

    void reset();
    char* read();
    void write(char* msg);

};

#endif //FLIGHT_ARDUINO_HPP
