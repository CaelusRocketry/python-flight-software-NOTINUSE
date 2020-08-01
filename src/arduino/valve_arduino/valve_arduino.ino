#include "ValveArduino.hpp"

#define BAUD 19200

ValveArduino valve_arduino;

void setup() {
    Serial.begin(BAUD);
    valve_arduino.registerSolenoids();
}

void loop() {
  valve_arduino.update();
}