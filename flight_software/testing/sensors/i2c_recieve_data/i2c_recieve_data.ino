/*
 LCD part reference to:
 http://www.arduino.cc/en/Tutorial/LiquidCrystal
 */

#include <Wire.h>
#define SLAVE_ADDRESS 0x04

void setup() {
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
  Serial.begin(9600);
}

void loop() {
}

void receiveEvent(int byteCount) {
  String s;
  int numOfBytes = Wire.available();
  byte b = Wire.read();  //cmd

  //print b?

  
  for(int i=0; i < numOfBytes - 1; i++){
    char data = Wire.read();
    s = s + data;
  }

  Serial.println(s);

  //String myString = (char*)myByteArray;
}
