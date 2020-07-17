#include "Arduino.h"
#include "Thermocouple.hpp"
#include "PressureSensor.hpp"
#include <stdint.h>
#include <Wire>

#ifndef SENSOR_ARDUINO_HPP
#define SENSOR_ARDUINO_HPP

class SensorArduino {
  private:
    // these maps map the pin to its respective sensor

    Thermocouple *thermocouples;
    PressureSensor *pressure_sensors;

    int num_thermocouples;
    int num_pressures;

    // send data to pi every 50 milliseconds
    const int SEND_DELAY = 50;

    void receiveData();
    void registerSensors();
    int recvI2CByte();

  public:
    SensorArduino();
    ~SensorArduino();
    void read();
    void sendData();
    void error();
};

#endif