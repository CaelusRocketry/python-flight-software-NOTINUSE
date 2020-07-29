#include "ValveArduino.hpp"

#define SLAVE_ADDRESS 0x08

ValveArduino valve_arduino();

void setup() {
    Serial.begin(9600);
    // Wire.begin(SLAVE_ADDRESS);
    // Wire.onReceive(receiveData);
    // Wire.onRequest(sendData);
}

void loop() {
  valve_arduino.update();
}

void receiveData(int byteCount){
  valve_arduino.receiveData(byteCount);
}

void sendData(){
  valve_arduino.sendData();
}