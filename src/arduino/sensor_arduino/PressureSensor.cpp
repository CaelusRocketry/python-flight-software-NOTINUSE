#include <PressureSensor.hpp>

#define MAX_PRESSURE 1000
#define ROOM_PRESSURE 15

float PressureSensor::mapVal(float val, float lower1, float upper1, float lower2, float upper2) {
    float diff1 = upper1 - lower1;
    float diff2 = upper2 - lower2;
    float factor = diff2 / diff1;
    return (val - lower1) * factor + lower2;
}

PressureSensor::PressureSensor() {
    pinMode(pressurePin, OUTPUT);
}

float PressureSensor::getPressure() {
    float analog = analogRead(pressurePin);
    float voltage = mapVal(analog, 0, 1023, 0, 5);
    float pressure = mapVal(voltage, 0.5, 4.5, 0, MAX_PRESSURE);
    return pressure + ROOM_PRESSURE;
}