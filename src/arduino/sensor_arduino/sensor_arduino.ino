#include "Arduino.h"
#include "SensorArduino.hpp"

#define SLAVE_ADDRESS 0x04

const int BAUD = 19200;
const int SEND_DATA_COMMAND = 255;

SensorArduino sensor_arduino;

void setup() {
  Serial.begin(BAUD);
  sensor_arduino.registerSensors();
}

void loop() {
  sensor_arduino.update();
  if(Serial.available()){
    int data = Serial.read();
    if(data == SEND_DATA_COMMAND){
      sensor_arduino.read();
    }
  }
  delay(100);
}
