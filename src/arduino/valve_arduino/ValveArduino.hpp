#include "Arduino.h"
// #include <Wire.h>
#include "Constants.hpp"
#include "Solenoid.hpp"

#ifndef VALVE_ARDUINO_HPP
#define VALVE_ARDUINO_HPP

class ValveArduino {
  private:
    Solenoid *solenoids;
    int numSolenoids;
    bool override;

    void launchBox();
    void ingestLaunchbox(int cmd, int data);

    int recvI2CByte();
    void registerSolenoids();

    void actuate(int pin, int actuationType);
    void checkSolenoids();

    void error(String error);

  public:
    ValveArduino();
    ~ValveArduino();
    void update();
    void receiveData(int byteCount);
    void sendData();
};

#endif