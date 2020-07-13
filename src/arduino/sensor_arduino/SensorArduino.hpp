#include <Thermocouple.hpp>
#include <PressureSensor.hpp>
#include <Wire.h>
#include <cstdint>

#ifndef SENSOR_ARDUINO_HPP
#define SENSOR_ARDUINO_HPP

class SensorArduino {
  private:
    // Sensor data variables
    double thermo_val;
    double pressure_val;
    double load_val;

    // Contains all three data variables
    struct sensorVars {
      double thermo;
      double pressure;
      double load;
    };

    // Temporary data storage
    sensorVars buffer[1000]{};
    int index;

    float getThermo();
    float getPressure();
    void receiveData();

    Thermocouple thermocouple;
    PressureSensor pressure_sensor;

  public:
    SensorArduino::SensorArduino();
    void read();
    void sendData();
};

#endif