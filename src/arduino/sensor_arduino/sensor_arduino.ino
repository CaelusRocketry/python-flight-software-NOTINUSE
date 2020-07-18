#include "Arduino.h"
#include "SensorArduino.hpp"
#include <Wire.h>

#define SLAVE_ADDRESS 0x04

SensorArduino sensor_arduino;

void setup() {
  Wire.onReceive(receiveData);
  Wire.onRequest(read);
  Wire.begin(SLAVE_ADDRESS);
}

void loop() {
  sensor_arduino.update();
}

void receiveData(int num_bytes){
  sensor_arduino.receiveData();
}

void read(){
  sensor_arduino.read();
}
