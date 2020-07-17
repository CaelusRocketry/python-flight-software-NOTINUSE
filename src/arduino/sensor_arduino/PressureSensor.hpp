#ifndef PRESSURE_SENSOR_HPP
#define PRESSURE_SENSOR_HPP

class PressureSensor {
    public:
        int pin;
        PressureSensor(int pin);
        float getPressure();
};

#endif