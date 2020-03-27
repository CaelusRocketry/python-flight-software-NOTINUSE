#include <Servo.h>
#include <Wire.h>

#define SLAVE_ADDRESS 0x08
// Pin definitions
#define NITROGEN_FILL 2
#define ETHANOL_DRAIN 3
#define ETHANOL_VENT 4
#define ETHANOL_MPV 5
#define NO_FILL 6
#define NO_DRAIN 7
#define NO_VENT 8
#define NO_MPV 9

boolean override = false;


void setup() {
  // put your setup code here, to run once:
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.begin(9600);
}

void loop() {
  if(override){
    launchBox();
  }
}

void launchBox(){
  
}

void pi(){

}

void receiveData(){
  if(override){
    return;
  }
}

void sendData(){

}

