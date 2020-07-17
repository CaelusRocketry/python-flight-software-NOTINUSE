#include "Thermocouple.hpp"

Thermocouple::Thermocouple(vector<int> pins) {
    this->pins = pins;
    maxthermo = new Adafruit_MAX31856(pins[0], pins[1], pins[2], pins[3]);
    maxthermo->begin();
}

Thermocouple::~Thermocouple() {
    delete maxthermo;
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
