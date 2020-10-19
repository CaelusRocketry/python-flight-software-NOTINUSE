#include "Arduino.h"
#include <SoftwareSerial.h>
#include "Constants.hpp"
#include "Solenoid.hpp"

#ifndef VALVE_ARDUINO_HPP
#define VALVE_ARDUINO_HPP

#define launchRX 2
#define launchTX 3
#define launchBaud 1200

class ValveArduino {
  private:
    Solenoid **solenoids;
    bool overrides;
    int numSolenoids;
    SoftwareSerial *launchSerial;

    void launchBox();
    void ingestLaunchbox(int cmd, int data);

    int recvSerialByte();

    void checkSolenoids();
    Solenoid* getSolenoid(int pin);
    int getSolenoidPos(int pin);

    void error(String error);

  public:
    ValveArduino();
    void start();
    ~ValveArduino();
    void registerSolenoids();
    void registerLaunchboxSolenoids();
    void update();
    void sendData();

    // make private after testing
    void actuate(int pin, int actuationType, bool from_launchbox);


};

#endif
