#include "ValveArduino.hpp"

ValveArduino::ValveArduino() {
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
    this->overrides = new bool[solenoidCount];

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

    Serial.write(REGISTERED_CONFIRMATION);

    // Serial.println("Registered");
}

int ValveArduino::getSolenoidPos(int pin){
    for(int i = 0; i < this->numSolenoids; i++){
        if(this->solenoids[i].pin == pin){
            return i;
        }
    }
    this->error("Could not find the indicated solenoid for pin " + pin);
    return -1;
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
            int pos = getSolenoidPos(pin);
            if (pin != -1 && !overrides[pos]) {
                actuate(pin, actuationType, false);
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
    launchBox();
}

Solenoid ValveArduino::getSolenoid(int pin){
    for(int i = 0; i < this->numSolenoids; i++){
        if(this->solenoids[i].pin == pin){
            return solenoids[i];
        }
    }
    this->error("Could not find the indicated solenoid for pin " + pin);
    return Solenoid(-1, false, false);
}

void ValveArduino::actuate(int pin, int actuationType, bool from_launchbox){
    Solenoid sol = getSolenoid(pin);
    if(sol.pin != -1 && (!sol.overridden || from_launchbox)){
        sol.actuate(actuationType);
    }
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
    if(cmd == L_DO_NOTHING){
        Solenoid sol = getSolenoid(data);
        if(sol.pin != -1) {
          sol.overridden = false;
        }
    }
    else{
        if(cmd == L_OPEN_VENT){
          cmd = OPEN_VENT;
        }
        else if(cmd == L_CLOSE_VENT){
          cmd = CLOSE_VENT;
        }
        else if(cmd == L_PULSE){
          cmd = PULSE;
        }
        actuate(data, cmd, true);
    }
}

void ValveArduino::error(String error) {
    digitalWrite(13, HIGH);
    // Serial.println(error);
}
