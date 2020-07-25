#include "Arduino.h"
#include "SensorArduino.hpp"
#include <Wire.h>

#define SLAVE_ADDRESS 0x04

SensorArduino sensor_arduino();

void setup() {
    Serial.begin(9600);
    Wire.onReceive(receiveData);
    Wire.onRequest(read);
    Wire.begin(SLAVE_ADDRESS);
}

void loop() {
    Serial.println("HI");
    sensor_arduino.update();
    delay(100);
}

void receiveData(int num_bytes){
  sensor_arduino.receiveData();
}

void read(){
  sensor_arduino.read();
}
