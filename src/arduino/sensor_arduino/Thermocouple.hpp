#include <vector>
#include <Adafruit_MAX31856.h>

#ifndef THERMOCOUPLE_HPP
#define THERMOCOUPLE_HPP

class Thermocouple {
    private:
        Adafruit_MAX31856 *maxthermo;
    public:
        vector<int> pins;
        Thermocouple::Thermocouple(vector<int> pins);
        Thermocouple::~Thermocouple();
        std::pair<float, bool> getTemp(); 
};

#endif