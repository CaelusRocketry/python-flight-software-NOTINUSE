#include "SensorArduino.hpp"

SensorArduino::SensorArduino() {
    // I2C initialization
    Serial.println("HI");
    pinMode(13, OUTPUT);
    registered = false;
}

void SensorArduino::receiveData(int num_bytes) {
    if(!registered){
        Serial.println("Registering!!!");
        registerSensors(num_bytes);
        registered = true;
    }
}

// TODO: make sure that the format matches what the pi is sending
// format: num_sensors, num_thermocouples, num_pressures, <for each sensor> 0 if thermocouple 1 if pressure, pin (or all four pins if its a thermocouple)
// example: 5, 2, 3, 1, 1, 1, 2, 1, 3, 0, 4, 5, 6, 7, 0, 8, 9, 10, 11
    // the first 3 pins are pressures, 4-7 is a thermocouple, 8-11 is a thermocouple

// 


int SensorArduino::recvI2CByte(){
    while(!Wire.available()){}
    return Wire.read();
}

void SensorArduino::registerSensors(int num_bytes) {
    Serial.print("Num bytes: ");
    Serial.println(num_bytes);
    int num_sensors = recvI2CByte();
    this->num_thermocouples = recvI2CByte();
    this->num_pressures = recvI2CByte();


    int thermocouple_len = 0;
    int pressure_len = 0;

    this->thermocouples[num_thermocouples];
    this->pressure_sensors[num_pressures];

    for(int i = 0; i < num_sensors; i++) {
        int sensor_type = recvI2CByte();
        Serial.print("Sensor type: ");
        Serial.println(sensor_type);
        if(sensor_type == 1) {
            int pin = recvI2CByte();
            Serial.println(pin);
            this->pressure_sensors[pressure_len] = PressureSensor(pin);
            pressure_len++;
        }
        else if(sensor_type == 0) {
            int pins[4];
            for(int i = 0; i < 4; i++){
                pins[i] = recvI2CByte();
            }
            this->thermocouples[thermocouple_len] = Thermocouple(pins);
            thermocouple_len++;
        }
        else {
            error();
        }
    }
}

void SensorArduino::update(){
    if(!registered){
        return;
    }
    for(int i = 0; i < this->num_thermocouples; i++) {
        thermocouples[i].updateTemp();
    }

    for(int i = 0; i < this->num_pressures; i++) {
        this->pressure_sensors[i].updatePressure();
    }
}

void SensorArduino::read() {
    for(int i = 0; i < this->num_thermocouples; i++) {
        sendData(thermocouples[i].pins[0], thermocouples[i].temp);
    }

    for(int i = 0; i < this->num_pressures; i++) {
        sendData(this->pressure_sensors[i].pin, pressure_sensors[i].pressure);
    }
}

void SensorArduino::sendData(int pin, float val) {
    union cvt {
        float val;
        unsigned char byte_array[4];
    } x;
    x.val = val;

    Wire.write(pin);
    Wire.write(x.byte_array, 4);
}

// Visual error for testing, turns LED on pin 13 on if there's an error
void SensorArduino::error(){
    digitalWrite(13, HIGH);
    Serial.println("Error");
}

SensorArduino::~SensorArduino() {
    delete[] thermocouples;
    delete[] pressure_sensors;
}