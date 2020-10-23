#include "ValveArduino.hpp"

ValveArduino *valve_arduino;
int actuated = false;

void setup() {
    Serial.begin(115200);
    valve_arduino = new ValveArduino();


    valve_arduino->registerSolenoids();
    //valve_arduino->registerLaunchboxSolenoids();
}

void loop() {
  valve_arduino->update();
  delay(100);

  if(millis() > 5000 && !actuated) {
    valve_arduino->actuate(4, 4, false);  //have made actuate a public method to test
    actuated = true;
  }
}
