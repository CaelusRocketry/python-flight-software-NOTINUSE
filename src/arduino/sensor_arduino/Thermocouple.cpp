#include "Thermocouple.hpp"

Thermocouple::Thermocouple(int pin1, int pin2, int pin3, int pin4) {
    this->pins = new int[4];
    this->pins[0] = pin1;
    this->pins[1] = pin2;
    this->pins[2] = pin3;
    this->pins[3] = pin4;

    maxthermo = new Adafruit_MAX31856(this->pins[0], this->pins[1], this->pins[2], this->pins[3]);
    maxthermo->begin();
}

Thermocouple::~Thermocouple() {
    delete maxthermo;
    delete[] pins;
}

float getTemp() {
    float temp = maxthermo->readThermocoupleTemperature();
    uint8_t fault = maxthermo->readFault();
    if(fault) {
        Serial.println("There's a fault in the thermocouple");
        digitalWrite(13, HIGH);
    }
    return temp;
}
