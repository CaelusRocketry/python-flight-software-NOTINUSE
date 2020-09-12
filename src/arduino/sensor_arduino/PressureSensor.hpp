#include "Arduino.h"

#ifndef PRESSURE_SENSOR_HPP
#define PRESSURE_SENSOR_HPP

#define MAX_PSI 1000
#define MIN_PSI 15
#define MIN_VOLTAGE 0.5
#define MAX_VOLTAGE 4.5


class PressureSensor {
    private:
        uint8_t pin;
        float pressure;
    public:
        PressureSensor() : pin(0), pressure(0){}
        PressureSensor(uint8_t myPin) : pin(myPin), pressure(0){
        }
        void updatePressure();
        int getPin();
        float getPressure();
};

#endif