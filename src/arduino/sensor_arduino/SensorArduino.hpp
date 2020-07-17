#include "Arduino.h"
#include "Thermocouple.hpp"
#include "PressureSensor.hpp"
#include <vector>
#include <string>
#include <cstdint>
#include <Wire>

#ifndef SENSOR_ARDUINO_HPP
#define SENSOR_ARDUINO_HPP

class SensorArduino {
  private:
    // these maps map the pin to its respective sensor

    std::vector<Thermocouple> thermocouples;
    std::vector<PressureSensor> pressure_sensors;

    // send data to pi every 50 milliseconds
    const int SEND_DELAY = 50;

    void receiveData();
    void registerSensors();
    int recvI2CByte();

  public:
    SensorArduino::SensorArduino();
    void read();
    void sendData();
    void error();
};

#endif