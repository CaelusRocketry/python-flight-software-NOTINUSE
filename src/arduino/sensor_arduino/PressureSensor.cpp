#include "PressureSensor.hpp"

float mapVal(float val, float lower1, float upper1, float lower2, float upper2) {
    float diff1 = upper1 - lower1;
    float diff2 = upper2 - lower2;
    float factor = diff2 / diff1;
    return (val - lower1) * factor + lower2;
}

float map_val(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void PressureSensor::updatePressure() {
    float pwmVal = analogRead(pin);
    // float voltage = mapVal(pwmVal, 0, 1023, 0, 5);
    // float base_pressure = mapVal(voltage, 0.5, 4.5, 0, MAX_PRESSURE);
    // pressure = base_pressure + ROOM_PRESSURE;

    float voltage = map_val(pwmVal, 0.00, 1024.00, 0.00, 5.00) + 0.0100;
    float psi = map_val(voltage, MIN_VOLTAGE, MAX_VOLTAGE, MIN_PSI, MAX_PSI);
    psi -= MIN_PSI;
    pressure = psi;
    // pressure = pwmVal;
}

int PressureSensor::getPin(){
    return this->pin;
}

float PressureSensor::getPressure(){
    return this->pressure;
}
