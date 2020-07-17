#include <ValveArduino.hpp>

void ValveArduino::error() {
    digitalWrite(13, HIGH);
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

ValveArduino::ValveArduino() {
    Wire.begin(SLAVE_ADDRESS);
    registerSolenoids();

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
    Serial.begin(9600);

    for(auto solenoid_pair : solenoids) {
        solenoid_states.emplace(solenoid_pair.first, NO_ACTUATION);
        pinMode(solenoid_pair.first, OUTPUT);
    }
    pinMode(13, OUTPUT);
}

void ValveArduino::registerSolenoids() {
    // reads from wire and fills the solenoids map with (pin, Solenoid) pairs
    // Solenoid constructor: Solenoid(int pin, bool isSpecial, bool isNO)
}

void ValveArduino::loop() {
    launchBox();
    pi();
}

void ValveArduino::receiveData(int byteCount) {
    while (Wire.available()) {
        int pin = Wire.read();
        int actuation_type = Wire.read();
        if (override) {
            break;
        }
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
                error();
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
    while (Serial.available() > 0) {
        int cmd = Serial.read();
        int data = Serial.read();
        ingestLaunchbox(cmd, data);
    }
}

void ValveArduino::pi() {
    // TODO: implement this
}