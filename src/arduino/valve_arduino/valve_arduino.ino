#include "ValveArduino.hpp"

#define SLAVE_ADDRESS 0x08

ValveArduino valve_arduino;

void setup() {
    Wire.begin(SLAVE_ADDRESS);
    Serial.begin(9600);
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
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