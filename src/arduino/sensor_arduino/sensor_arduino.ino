#include "Arduino.h"
#include "SensorArduino.hpp"

const int SEND_DATA_COMMAND = 255;

SensorArduino sensor_arduino;

void setup() {
  Serial.begin(115200);
  sensor_arduino.registerSensors();
}

void loop() {
  // Updates the sensor arduino and checks if any commands were sent from the serial.
  sensor_arduino.update();

  if (Serial.available()) {
    int data = Serial.read();
    if (data == SEND_DATA_COMMAND) {
      sensor_arduino.read();
    }
  }
}
