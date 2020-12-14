#include "Arduino.h"

// Include guard
#ifndef PRESSURE_SENSOR_HPP
#define PRESSURE_SENSOR_HPP

// Minimum/maximum PSI
#define MIN_PSI 15
#define MAX_PSI 1000

// Minimum/maximum voltage
#define MIN_VOLTAGE 0.5
#define MAX_VOLTAGE 4.5

/**
 * Wrapper class for a pressure sensor.
 * Stores the pin and the most recently read pressure value.
 * 
 */
class PressureSensor {
    private:
        uint8_t pin = 0;
        float pressure = 0;
    public:
        /**
         * Default constructor. Sets the pin to 0.
         */
        PressureSensor() {}

        /**
         * Constructor that allows you to specify the pin.
         * @param pin_ The pin this sensor is routed to.
         */
        PressureSensor(uint8_t pin_): pin(pin_) {}

        void updatePressure();

        // Basis getter methods
        int getPin();
        float getPressure();
};

#endif