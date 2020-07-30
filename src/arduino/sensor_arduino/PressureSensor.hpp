#include "Arduino.h"

#ifndef PRESSURE_SENSOR_HPP
#define PRESSURE_SENSOR_HPP

#define MAX_PRESSURE 1000
#define ROOM_PRESSURE 15

class PressureSensor {
    private:
        uint8_t pin;
        float pressure;
    public:
        PressureSensor() : pin(0), pressure(0){}
        PressureSensor(uint8_t myPin) : pin(myPin), pressure(0){
            pinMode(pin, OUTPUT);
        }
        void updatePressure();
        int getPin();
        float getPressure();
};

#endif