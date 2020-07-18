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

int ValveArduino::recvI2CByte() {
    while(!Wire.available()){}
    return Wire.read();
}

// TODO: make sure that the format matches what the pi is sending
// format: num_solenoids, <for each solenoid> pin, isSpecial, isNO
// ex: 4, 1, 1, 1, 2, 0, 1, 3, 0, 0, 4, 1, 0

void ValveArduino::registerSolenoids() {
    int solenoid_count = recvI2CByte();
    this->num_solenoids = solenoid_count;
    this->solenoids = new Solenoid[solenoid_count];

    for(int i = 0; i < solenoid_count; i++) {
        int pin = recvI2CByte();
        bool isSpecial = recvI2CByte();
        bool isNO = recvI2CByte();
        this->solenoids[i] = Solenoid(pin, isSpecial, isNO);
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

// TODO: make sure the pi is receiving this in the right format
// format: <for each solenoid> pin, isOpen, actuation_type

void ValveArduino::sendData() {
    for(int i = 0; i < this->num_solenoids; i++) {
        Wire.write(this->solenoids[i].getPin());
        Wire.write(this->solenoids[i].getStatus());
        Wire.write(this->solenoids[i].getActuation());
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

void ValveArduino::pi() {
    // TODO: implement this
}

ValveArduino::~ValveArduino() {
    delete[] solenoids;
}