#include <SensorArduino.hpp>

#define SLAVE_ADDRESS 0x04

SensorArduino::SensorArduino() {
    // I2C initialization
    Wire.begin(SLAVE_ADDRESS);
    registerSensors();

    Wire.onReceive(receiveData);
    Wire.onRequest(read);
    Serial.begin(9600);
    pinMode(13, OUTPUT);
}

void SensorArduino::receiveData() {
    
}

// TODO: make sure that the format matches what the pi is sending
// format: num_sensors, num_thermocouples, num_pressures, <for each sensor> 0 if thermocouple 1 if pressure, pin (or all four pins if its a thermocouple)
// example: 5, 2, 3, 1, 1, 1, 2, 1, 3, 0, 4, 5, 6, 7, 0, 8, 9, 10, 11
    // the first 3 pins are pressures, 4-7 is a thermocouple, 8-11 is a thermocouple

int SensorArduino::recvI2CByte(){
    while(!Wire.available()){}
    return Wire.read();
}

void SensorArduino::registerSensors() {
    int num_sensors = recvI2CByte();
    this->num_thermocouples = recvI2CByte();
    this->num_pressures = recvI2CByte();

    int thermocouple_len = 0;
    int pressure_len = 0;

    this->thermocouples = new Thermocouple[this->num_thermocouples];
    this->pressure_sensors = new PressureSensor[this->num_pressures];

    for(int i = 0; i < num_sensors; i++) {
        int sensor_type = recvI2CByte();
        if(sensor_type == 1) {
            int pin = recvI2CByte();
            this->pressure_sensors[pressure_len] = PressureSensor(pin);
            pressure_len++;
        }
        else if(sensor_type == 0) {
            this->thermocouples[thermocouple_len] = Thermocouple(recvI2CByte(), recvI2CByte(), recvI2CByte(), recvI2CByte());
            thermocouple_len++;
        }
        else {
            error();
        }
    }
}

void SensorArduino::read() {
    for(int i = 0; i < this->num_thermocouples; i++) {
        float thermo_val = thermocouples[i].getThermo();
        sendData(thermocouples[i].pins[0], thermo_val);
    }

    for(int i = 0; i < this->num_pressures; i++) {
        float pressure_val = this->pressure_sensors[i].getPressure();
        sendData(this->pressure_sensors[i].pin, pressure_val);
    }

    delay(SEND_DELAY);
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