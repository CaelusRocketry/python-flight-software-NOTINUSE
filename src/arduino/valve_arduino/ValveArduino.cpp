#include "ValveArduino.hpp"


ValveArduino::ValveArduino() {
    registerSolenoids();
    override = false;
    pinMode(13, OUTPUT);
}

ValveArduino::~ValveArduino() {
    delete[] solenoids;
}

int ValveArduino::recvI2CByte() {
    return Serial.read();
}

// TODO: make sure that the format matches what the pi is sending
// format: numSolenoids, <for each solenoid> pin, isSpecial, isNO
// ex: 4, 1, 1, 1, 2, 0, 1, 3, 0, 0, 4, 1, 0

void ValveArduino::registerSolenoids() {
    int solenoidCount = recvI2CByte();
    this->numSolenoids = solenoidCount;
    this->solenoids[solenoidCount];

    for(int i = 0; i < solenoidCount; i++) {
        int pin = recvI2CByte();
        int special = recvI2CByte();
        int natural = recvI2CByte();
        bool isSpecial = true; bool isNO = true;
        if(special == 0){
            isSpecial = false;
        }
        if(natural == 0){
            isNO = false;
        }
        this->solenoids[i] = Solenoid(pin, isSpecial, isNO);
    }
}

void ValveArduino::checkSolenoids() {
    for(int i = 0; i < numSolenoids; i++) {
        solenoids[i].control();
    }
}

void ValveArduino::update() {
    checkSolenoids();
    // TODO: Uncomment this
    // launchBox();
}

void ValveArduino::actuate(int pin, int actuationType){
    for(int i = 0; i < this->numSolenoids; i++){
        if(this->solenoids[i].pin == pin){
            this->solenoids[i].actuate(actuationType);
            return;
        }
    }
    this->error("Could not find the indicated solenoid for pin " + pin);
}

void ValveArduino::receiveData(int byteCount) {
    while (Wire.available()) {
        int pin = Wire.read();
        int actuationType = Wire.read();
        if (override) {
            break;
        }
        actuate(pin, actuationType);
    }
}

// TODO: make sure the pi is receiving this in the right format
// format: <for each solenoid> pin, isOpen, actuationType

void ValveArduino::sendData() {
    for(int i = 0; i < this->numSolenoids; i++) {
        Serial.print(this->solenoids[i].pin);
        Serial.print(this->solenoids[i].getState());
        Serial.print(this->solenoids[i].actuation);
    }
}

void ValveArduino::launchBox() {
    // TODO: Change this to use SoftwareSerial
    while (Serial.available() > 0) {
        int cmd = Serial.read();
        int data = Serial.read();
        ingestLaunchbox(cmd, data);
    }
}


void ValveArduino::ingestLaunchbox(int cmd, int data) {
    if (cmd == DATA) {
        if (data == OVERRIDE) {
            override = true;
        } else if (data == OVERRIDE_UNDO) {
            override = false;
        } else {
            error("Unknown data received via launchbox");
        }
        return;
    }
    if (!override) {
        return;
    }
    actuate(data, cmd);
}

void ValveArduino::error(String error) {
    digitalWrite(13, HIGH);
    // Serial.println(error);
}
