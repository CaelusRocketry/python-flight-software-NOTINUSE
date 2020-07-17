#include <Thermocouple.hpp>

Thermocouple::Thermocouple(vector<int> pins) {
    maxthermo = new Adafruit_MAX31856(pins[0], pins[1], pins[2], pins[3]);
    maxthermo->begin();
}

std::pair<float, bool> getTemp() {
    float temp = maxthermo->readThermocoupleTemperature();
    uint8_t fault = maxthermo->readFault();
    bool fault_ret = false;
    if(fault) {
        fault_ret = true;
    }
    return std::make_pair(temp, fault_ret);
}

Thermocouple::~Thermocouple() {
    delete maxthermo;
}