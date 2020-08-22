#include "SensorArduino.hpp"

SensorArduino::SensorArduino() {
    pinMode(13, OUTPUT);
    registered = false;
}

// TODO: make sure that the format matches what the pi is sending
// format: num_sensors, num_thermocouples, num_pressures, <for each sensor> 0 if thermocouple 1 if pressure, pin (or all four pins if its a thermocouple)
// example: 5, 2, 3, 1, 1, 1, 2, 1, 3, 0, 4, 5, 6, 7, 0, 8, 9, 10, 11
    // the first 3 pins are pressures, 4-7 is a thermocouple, 8-11 is a thermocouple

int SensorArduino::recvSerialByte(){
    while(!Serial.available()){}
    int ret = Serial.read();

    return ret;
}

void SensorArduino::registerSensors() {
    int num_sensors = recvSerialByte();
    this->num_thermocouples = recvSerialByte();
    this->num_pressures = recvSerialByte();

    int thermocouple_len = 0;
    int pressure_len = 0;

    this->thermocouples = new Thermocouple[num_thermocouples];
    this->pressure_sensors = new PressureSensor[num_pressures];

    for(int i = 0; i < num_sensors; i++) {
        int sensor_type = recvSerialByte();
        if(sensor_type == 1) {
            int pin = recvSerialByte();
            pinMode(pin, INPUT);
            this->pressure_sensors[pressure_len] = PressureSensor(pin);
            pressure_len++;
        }
        else if(sensor_type == 0) {
            int pins[4];
            for(int i = 0; i < 4; i++){
                pins[i] = recvSerialByte();
            }
            this->thermocouples[thermocouple_len] = Thermocouple(pins);
            thermocouple_len++;
        }
        else {
            error();
        }
    }
    registered = true;
    // Return signal saying that all the sensors were successfully registered
    Serial.write(255);
//    Serial.println(255);
}

void SensorArduino::update(){
    if(!registered){
        return;
    }
    for(int i = 0; i < num_thermocouples; i++) {
        thermocouples[i].updateTemp();
    }

    for(int i = 0; i < num_pressures; i++) {
        pressure_sensors[i].updatePressure();
    }
}

void SensorArduino::read() {
    for(int i = 0; i < this->num_thermocouples; i++) {
        sendData(thermocouples[i].pins[0], thermocouples[i].getTemp());
    }

    for(int i = 0; i < this->num_pressures; i++) {
        sendData(this->pressure_sensors[i].getPin(), pressure_sensors[i].getPressure());
    }
}

void SensorArduino::sendData(int pin, float val) {
    union cvt {
        float val;
        unsigned char byte_array[4];
    } x;
    x.val = val;

    Serial.write(pin);
    // Serial.println(val);
    for(int i = 0; i < 4; i++){
        Serial.write(x.byte_array[i]);
    }
}

// Visual error for testing, turns LED on pin 13 on if there's an error
void SensorArduino::error(){
    digitalWrite(13, HIGH);
}

SensorArduino::~SensorArduino() {
    delete[] thermocouples;
    delete[] pressure_sensors;
}
