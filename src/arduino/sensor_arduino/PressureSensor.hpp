#include "Arduino.h"

#ifndef PRESSURE_SENSOR_HPP
#define PRESSURE_SENSOR_HPP

class PressureSensor {
    public:
        int pin;
        float pressure;
        PressureSensor(int pin);
        void updatePressure();
};

#endif