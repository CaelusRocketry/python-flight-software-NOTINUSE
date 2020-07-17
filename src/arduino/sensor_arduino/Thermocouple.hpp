#include <Adafruit_MAX31856.h>

#ifndef THERMOCOUPLE_HPP
#define THERMOCOUPLE_HPP

class Thermocouple {
    private:
        Adafruit_MAX31856 *maxthermo;
    public:
        int *pins;
        Thermocouple(int pin1, int pin2, int pin3, int pin4);
        ~Thermocouple();
        float getTemp(); 
};

#endif