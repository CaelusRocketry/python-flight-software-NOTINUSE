#include <utility>
#include <Adafruit_MAX31856.h>

#ifndef THERMOCOUPLE_HPP
#define THERMOCOUPLE_HPP

class Thermocouple {
    private:
        Adafruit_MAX31856 maxthermo(10, 11, 12, 13);
    public:
        Thermocouple::Thermocouple();
        std::pair<float, bool> getTemp(); 
};

#endif