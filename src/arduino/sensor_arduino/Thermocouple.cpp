#include <Thermocouple.hpp>

Thermocouple::Thermocouple() {
    maxthermo.begin();
}

std::pair<float, bool> getTemp() {
    float temp = maxthermo.readThermocoupleTemperature();
    uint8_t fault = maxthermo.readFault();
    bool fault_ret = false;
    if(fault) {
        fault_ret = true;
    }
    return std::make_pair(temp, fault_ret);
}