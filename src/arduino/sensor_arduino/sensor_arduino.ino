#include <SensorArduino.hpp>

SensorArduino sensor_arduino = SensorArduino();

void setup() {

}

void loop() {
  sensor_arduino.read();
}