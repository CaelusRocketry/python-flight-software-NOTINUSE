#include "Thermocouple.hpp"

Thermocouple::Thermocouple(int *pins) {
    for(int i = 0; i < 4; i++){
        this->pins[i] = pins[i];
    }

    maxthermo = new Adafruit_MAX31856(pins[0], pins[1], pins[2], pins[3]);
    maxthermo->begin();
    temp = 0;
}

Thermocouple::~Thermocouple() {
    delete maxthermo;
    delete[] pins;
}

void Thermocouple::updateTemp() {
    float curr_temp = maxthermo->readThermocoupleTemperature();
    uint8_t fault = maxthermo->readFault();
    if(fault) {
        // Serial.println("There's a fault in the thermocouple");
        digitalWrite(13, HIGH);
        return;
    }
    temp = curr_temp;
}
