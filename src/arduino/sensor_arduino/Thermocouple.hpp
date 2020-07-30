#include "Arduino.h"
#include <Adafruit_MAX31856.h>

#ifndef THERMOCOUPLE_HPP
#define THERMOCOUPLE_HPP

class Thermocouple {
    private:
        Adafruit_MAX31856 *maxthermo;
        float temp;
    public:
        int *pins;
        Thermocouple(){};
        Thermocouple(int *pins);
        ~Thermocouple();
        void updateTemp();
        float getTemp();
};

#endif