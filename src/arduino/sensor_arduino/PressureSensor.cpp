#include "PressureSensor.hpp"

#define MAX_PRESSURE 1000
#define ROOM_PRESSURE 15

PressureSensor::PressureSensor(uint8_t pin) {
    pressure = 0;
    this->pin = pin;
    this->pin2 = &pin;
    pinMode(this->pin, OUTPUT);
    Serial.println(this->pin);
}

float mapVal(float val, float lower1, float upper1, float lower2, float upper2) {
    float diff1 = upper1 - lower1;
    float diff2 = upper2 - lower2;
    float factor = diff2 / diff1;
    return (val - lower1) * factor + lower2;
}

void PressureSensor::updatePressure() {
    Serial.println(this->pin);
    float pwmVal = analogRead(pin);
    float voltage = mapVal(pwmVal, 0, 1023, 0, 5);
    float base_pressure = mapVal(voltage, 0.5, 4.5, 0, MAX_PRESSURE);
    pressure = base_pressure + ROOM_PRESSURE;
}

int PressureSensor::getPin(){
    return pin;
}
