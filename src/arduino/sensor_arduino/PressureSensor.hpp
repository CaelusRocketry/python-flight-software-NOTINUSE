#include "Arduino.h"

#ifndef PRESSURE_SENSOR_HPP
#define PRESSURE_SENSOR_HPP

class PressureSensor {
    private:
        uint8_t pin;
        int *pin2;
    public:
        float pressure;
        PressureSensor(int pin);
        void updatePressure();
        int getPin();
};

#endif