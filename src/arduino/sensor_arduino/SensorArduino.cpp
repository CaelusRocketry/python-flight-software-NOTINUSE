#include <SensorArduino.hpp>

#define SLAVE_ADDRESS 0x04

SensorArduino::SensorArduino() {
    // I2C initialization
    Wire.begin(SLAVE_ADDRESS);
    registerSensors();

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
    Serial.begin(9600);
    pinMode(13, OUTPUT);
}

void SensorArduino::receiveData() {
    
}

// TODO: make sure that the format matches what the pi is sending
// format: num_sensors, <for each sensor> 0 if thermocouple 1 if pressure, pin (or all four pins if its a thermocouple)
// example: 5, 1, 1, 1, 2, 1, 3, 0, 4, 5, 6, 7, 0, 8, 9, 10, 11
    // the first 3 pins are pressures, 4-7 is a thermocouple, 8-11 is a thermocouple

int SensorArduino::recvI2CByte(){
    while(!Wire.available()){}
    return Wire.read();
}

void SensorArduino::registerSensors() {
    int num_sensors = recvI2CByte();
    for(int i = 0; i < num_sensors; i++){
        int sensor_type = recvI2CByte();
        if(sensor_type == 1){
            int pin = recvI2CByte();
            pressure_sensors.push_back(PressureSensor(pin));
        }
        else if(sensor_type == 0){
            std::vector<int> pins;
            for(int i = 0; i < 4; i++) {
                pins.push_back(recvI2CByte());
            }
            thermocouples.push_back(Thermocouple(pins))            
        }
        else{
            error();
        }
    }
}

void SensorArduino::read() {
    for(auto thermocouple : thermocouples) {
        float thermo_val = thermocouple.getThermo();
        sendData(thermocouple.pins[0], thermo_val);
    }

    for(auto pressure_pair : pressure_sensors) {
        float pressure_val = pressure_sensor.getPressure();
        sendData(pressure_sensor.pin, pressure_val);
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
void SensorArduino::error(std::string msg){
    digitalWrite(13, HIGH);
    Serial.println("Error message: " + msg);
}
