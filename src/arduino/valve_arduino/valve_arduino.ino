#include <Servo.h>
#include <Wire.h>

#define SLAVE_ADDRESS 0x08
Servo motor;

void setup() {
  // put your setup code here, to run once:
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  motor.attach(3);
}

void loop() {
}

void receiveData(){
  
}

void sendData(){

}

