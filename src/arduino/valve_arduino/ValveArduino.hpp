#include <Servo.h>
#include <Wire.h>
#include <Arduino.h>
#include <ArduinoSTL.h>
#include <stdint.h>
#include <map>
#include <Solenoid.hpp>

#ifndef VALVE_ARDUINO_HPP
#define VALVE_ARDUINO_HPP

// Pin definitions

class ValveArduino {
  private:
    // maps pin numbers to the respective Solenoid
    std::map<int, Solenoid> solenoids;

    // maps pin numbers to the respective solenoid state
    std::map<int, Solenoid> solenoid_states;

    // Serial/I2C definitions. MAKE SURE CLOSE_VENT, OPEN_VENT, PULSE MATCH WHATEVER'S IN valve_task.py
    const int DATA = 0;
    const int NO_ACTUATION = 0;
    const int CLOSE_VENT = 1;
    const int OPEN_VENT = 2;
    const int PULSE = 3;
    const int OVERRIDE = 0;
    const int OVERRIDE_UNDO = 1;

    // Timing stuff
    const int OPEN_CYCLE = 4;
    const int OPEN_CYCLE_CLOSE = 2;
    const int PULSE_TIME = 1;
    bool override = false;

    void error();
    void close(int pin);
    void open(int pin);
    void pulse(int pin);
    void ingestLaunchbox(int cmd, int data);
    void receiveData(int byteCount);
    void sendData();
    void launchBox();
    void pi();
    void registerSolenoids();
    void checkSolenoids();

  public:
    ValveArduino();
    void update();
};

#endif