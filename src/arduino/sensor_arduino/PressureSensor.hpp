#include <Arduino.h>

#ifndef PRESSURE_SENSOR_HPP
#define PRESSURE_SENSOR_HPP

class PressureSensor {
    private:
        float mapVal(float val, float lower1, float upper1, float lower2, float upper2);
        const int pressurePin = A1;

    public:
        PressureSensor();
        float getPressure();
};

#endif