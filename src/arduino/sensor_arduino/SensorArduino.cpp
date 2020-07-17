#include <SensorArduino.hpp>

#define SLAVE_ADDRESS 0x04

float SensorArduino::getThermo(int pin) {
    auto thermo_ret = thermocouples[pin].getTemp();

    if(thermo_ret.second) {
        Serial.println("There's a fault in the thermocouple");
    }

    return thermo_ret.first;
}

float SensorArduino::getPressure(int pin) {
    return pressure_sensors[pin].getPressure();
}

void SensorArduino::receiveData() {
    
}

SensorArduino::SensorArduino() {
    // I2C initialization
    Wire.begin(SLAVE_ADDRESS);
    registerSensors();

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
    Serial.begin(9600);
}

// TODO: make sure that the format matches what the pi is sending
// format: pin (or the first of four consecutive pins if it a thermocouple), 0 if thermocouple 1 if pressure
// example: 1121314080
    // the first 3 pins are pressures, 4-7 is a thermocouple, 8-11 is a thermocouple

void SensorArduino::registerSensors() {
    while(Wire.available()) {
        int pin = Wire.read();
        bool isPressure = Wire.read();
        if(isPressure) {
            pressure_sensors.emplace(pin, PressureSensor(pin))
        }  
        else {
            std::vector<int> pins;
            for(int i = pin; i < pin + 4; i++) {
                pins.push_back(i);
            }

            thermocouples.emplace(pin, Thermocouple(pins))
        }
    }
}

void SensorArduino::read() {
    for(auto thermocouple_pair : thermocouples) {
        float thermo_val = getThermo(thermocouple_pair.first);
        sendData(thermocouple_pair.first, false, thermo_val);
    }

    for(auto pressure_pair : pressure_sensors) {
        float pressure_val = getPressure(pressure_pair.first);
        sendData(pressure_pair.first, true, pressure_val);
    }

    std::this_thread::sleep_for(std::chrono::milliseconds(SEND_DELAY));
}

// TODO: make sure this format (pin (or the first of four consecutive pins if it a thermocouple), 1 if pressure else 0, value) matches up w the pi

void SensorArduino::sendData(int pin, bool isPressure, float val) {
    union cvt {
        float val;
        unsigned char byte_array[4];
    } x;
    x.val = val;

    Wire.write(pin)
    Wire.write(isPressure)
    Wire.write(x.byte_array, 4);
}
