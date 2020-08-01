#include "Arduino.h"
#include <SoftwareSerial.h>
#include "Constants.hpp"
#include "Solenoid.hpp"

#ifndef VALVE_ARDUINO_HPP
#define VALVE_ARDUINO_HPP

#define launchRX 2
#define launchTX 3
#define launchBaud 19200

class ValveArduino {
  private:
    Solenoid *solenoids;
    int numSolenoids;
    bool override;
    SoftwareSerial *launchSerial;

    void launchBox();
    void ingestLaunchbox(int cmd, int data);

    int recvSerialByte();

    void actuate(int pin, int actuationType);
    void checkSolenoids();

    void error(String error);

  public:
    ValveArduino();
    ~ValveArduino();
    void registerSolenoids();
    void update();
    void sendData();
};

#endif