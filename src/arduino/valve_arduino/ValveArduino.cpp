#include "ValveArduino.hpp"


ValveArduino::ValveArduino() {
    override = false;
    pinMode(13, OUTPUT);
    launchSerial = new SoftwareSerial(launchRX, launchTX);
    launchSerial->begin(launchBaud);
}

ValveArduino::~ValveArduino() {
    delete[] solenoids;
}

int ValveArduino::recvSerialByte() {
    while(!Serial.available()){}
    int ret = Serial.read();
    // Serial.write(ret);
    return ret;
}

// TODO: make sure that the format matches what the pi is sending
// format: numSolenoids, <for each solenoid> pin, isSpecial, isNO
// ex: 4, 1, 1, 1, 2, 0, 1, 3, 0, 0, 4, 1, 0
// ex: 1, 2, 1, 1

void ValveArduino::registerSolenoids() {
    int solenoidCount = recvSerialByte();
    this->numSolenoids = solenoidCount;
    this->solenoids = new Solenoid[solenoidCount];

    for(int i = 0; i < solenoidCount; i++) {
        int pin = recvSerialByte();
        int special = recvSerialByte();
        int natural = recvSerialByte();
        bool isSpecial = true;
        bool isNO = true;
        if(special == 0){
            isSpecial = false;
        }
        if(natural == 0){
            isNO = false;
        }
        this->solenoids[i] = Solenoid(pin, isSpecial, isNO);
    }

    // Serial.println("Registered");
}

void ValveArduino::checkSolenoids() {
    if(Serial.available()) {
        int cmd = recvSerialByte();
        if(cmd == SEND_DATA_CMD){
            sendData();
        }
        else if(cmd == ACTUATE_CMD){
            int pin = recvSerialByte();
            int actuationType = recvSerialByte();
            if (!override) {
                actuate(pin, actuationType);
            }
        }
        else{
            error("Unknown command received");
        }
    }
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

// TODO: make sure the pi is receiving this in the right format
// format: <for each solenoid> pin, isOpen, actuationType

void ValveArduino::sendData() {
    for(int i = 0; i < this->numSolenoids; i++) {
        Serial.write(this->solenoids[i].pin);
        Serial.write(this->solenoids[i].getState()); // 1 if open else 0
        Serial.write(this->solenoids[i].getActuation());
    }
}

void ValveArduino::launchBox() {
    // TODO: Change this to use SoftwareSerial
    if(launchSerial->available()) {
        int cmd = launchSerial->read();
        int data = launchSerial->read();
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
