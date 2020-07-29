#include "Arduino.h"
#include "Thermocouple.hpp"
#include "PressureSensor.hpp"
#include <stdint.h>

#ifndef SENSOR_ARDUINO_HPP
#define SENSOR_ARDUINO_HPP

class SensorArduino {
  private:
    // these maps map the pin to its respective sensor

    Thermocouple *thermocouples;

    int num_thermocouples;
    int num_pressures;

    // send data to pi every 50 milliseconds
    const int SEND_DELAY = 50;

    int recvSerialByte();
    bool registered = false;

  public:
    SensorArduino();
    ~SensorArduino();
    PressureSensor *pressure_sensors;
    void registerSensors();
    void read();
    void update();
    void sendData(int pin, float val);
    void error();
};

#endif