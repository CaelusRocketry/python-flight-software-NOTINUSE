#include <Thermocouple.hpp>
#include <PressureSensor.hpp>
#include <map>
#include <Wire.h>
#include <chrono>
#include <thread>
#include <cstdint>

#ifndef SENSOR_ARDUINO_HPP
#define SENSOR_ARDUINO_HPP

class SensorArduino {
  private:
    // these maps map the pin to its respective sensor

    std::map<int, Thermocouple> thermocouples;
    std::map<int, PressureSensor> pressure_sensors;

    // send data to pi every 50 milliseconds
    const int SEND_DELAY = 50;

    float getThermo();
    float getPressure();
    void receiveData();
    void registerSensors();

  public:
    SensorArduino::SensorArduino();
    void read();
    void sendData();
};

#endif