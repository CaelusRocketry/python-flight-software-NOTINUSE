#include <ValveArduino.hpp>


ValveArduino::ValveArduino() {
    registerSolenoids();

    for(auto solenoid_pair : solenoids) {
        solenoid_states.emplace(solenoid_pair.first, NO_ACTUATION);
        pinMode(solenoid_pair.first, OUTPUT);
    }
    pinMode(13, OUTPUT);
}


void ValveArduino::error(String error) {
    digitalWrite(13, HIGH);
    Serial.println(error);
}

void ValveArduino::close(int pin) {
    solenoids[pin].close();
}

void ValveArduino::open(int pin) {
    solenoids[pin].open()
}

void ValveArduino::pulse(int pin) {
    solenoids[pin].pulse();
}

void ValveArduino::ingestLaunchbox(int cmd, int data) {
    if (cmd == DATA) {
        if (data == OVERRIDE) {
            override = true;
        } else if (data == OVERRIDE_UNDO) {
            override = false;
        } else {
            error();
        }
        return;
    }
    if (!override) {
        return;
    }
    switch (cmd) {
        case CLOSE_VENT:
            solenoid_states[data] = CLOSE_VENT;
            close(data);
            break;
        case OPEN_VENT:
            solenoid_states[data] = OPEN_VENT;
            open(data);
            break;
        case PULSE:
            solenoid_states[data] = PULSE;
            pulse(data);
            break;
        default:
            error();
            break;
    }
}

// TODO: make sure that the format matches what the pi is sending

void ValveArduino::registerSolenoids() {
    while(Wire.available()) {
        int pin = Wire.read();
        bool isSpecial = Wire.read();
        bool isNO = Wire.read();
        Solenoid mySolenoid = Solenoid(pin, isSpecial, isNO);    
        solenoids.insert(std::pair<int, Solenoid>(pin, mySolenoid));   
    }
}

void ValveArduino::checkSolenoids() {
    for(auto solenoid_pair : solenoids) {
        Solenoid sol = solenoid_pair.second;
        if(sol.getStatus() && sol.getSpecial()) {
            sol.controlOpen();
        }
        else if(sol.getPulse()) {
            sol.controlPulse();
        }
    }
}

void ValveArduino::update() {
    checkSolenoids();
    // TODO: Uncomment this
    // launchBox();
    pi();
}

void ValveArduino::actuate(int pin, int actuation_type){
    switch (actuation_type) {
        case NO_ACTUATION:
            solenoid_states[pin] = NO_ACTUATION;
            break;
        case CLOSE_VENT:
            solenoid_states[pin] = CLOSE_VENT;
            close(pin);
            break;
        case OPEN_VENT:
            solenoid_states[pin] = OPEN_VENT;
            open(pin);
            break;
        case PULSE:
            solenoid_states[pin] = PULSE;
            pulse(pin);
            break;
        default:
            error("Unknown actuation type");
            break;
    }
}

void ValveArduino::receiveData(int byteCount) {
    while (Wire.available()) {
        int pin = Wire.read();
        int actuation_type = Wire.read();
        if (override) {
            break;
        }
    }
}

void ValveArduino::sendData() {
    unsigned long data = 0;
    if (override) {
        data = 1;
    }
    for (auto solenoid_pair : solenoids) {
        int state = solenoid_states[solenoid_pair.first]
        data = data | (state << (valve * 2 + 1))
    }
    uint8_t buf[4];
    buf[0] = (uint8_t) data;
    buf[1] = (uint8_t) data >> 8;
    buf[2] = (uint8_t) data >> 16;
    buf[3] = (uint8_t) data >> 24;
    Wire.write(buf, 4);
}

void ValveArduino::launchBox() {
    // TODO: Change this to use SoftwareSerial
    while (Serial.available() > 0) {
        int cmd = Serial.read();
        int data = Serial.read();
        ingestLaunchbox(cmd, data);
    }
}

void ValveArduino::pi() {
    // TODO: implement this
}
