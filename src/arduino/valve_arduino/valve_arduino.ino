#include "ValveArduino.hpp"

ValveArduino valve_arduino;

void setup() {
    Serial.begin(115200);
    valve_arduino.registerSolenoids();
}

void loop() {
  valve_arduino.update();
}