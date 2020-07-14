#include <ValveArduino.hpp>

void ValveArduino::error() {
    digitalWrite(13, HIGH);
}

void ValveArduino::close(int pin) {
    digitalWrite(pin, LOW);
    states[i] = CLOSE_VENT;
    times[i] = -1;
}

void ValveArduino::open(int pin) {
    digitalWrite(pin, HIGH);
    states[i] = OPEN_VENT;
    times[i] = millis() + OPEN_CYCLE;
}

void ValveArduino::pulse(int pin) {
    open(pin);
    states[i] = PULSE;
    times[i] = millis() + PULSE_TIME;
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
        close(data);
        break;
    case OPEN_VENT:
        open(data);
        break;
    case PULSE:
        pulse(data);
        break;
    default:
        error();
        break;
    }
}

ValveArduino::ValveArduino() {
    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
    Serial.begin(9600);
    for (int i = 0; i < NUM_VALVES; i++) {
        pinMode(ALL_PINS[i], OUTPUT);
    }
    for (int i = 0; i < MAX_PIN; i++) {
        times[i] = -1;
        states[i] = CLOSE_VENT;
    }
    pinMode(13, OUTPUT);
}

void ValveArduino::loop() {
    // Valve open cycle control and pulse control
    for (int i = 0; i < NUM_STATES; i++) {
        if (times[i] == -1) {
            continue;
        }
        if (millis() > times[i]) {
            if (states[i] == PULSE) {
                close(i);
            } else if (states[i] == OPEN_VENT) {
                close(i);
                times[i] = millis() + OPEN_CYCLE_CLOSE;
            } else if (states[i] == CLOSE_VENT) {
                open(i);
            } else {
                error();
            }
        }
    }
    launchBox();
    pi();
}

void ValveArduino::receiveData(int byteCount) {
    while (Wire.available()) {
        int loc_idx = Wire.read();
        int actuation_type = Wire.read();
        if (override) {
            return;
        }
        int valve_pin = ALL_PINS[loc_idx];
        switch (actuation_type) {
        case NO_ACTUATION:
            actuation_on[valve_pin] = false;
        case CLOSE_VENT:
            close(valve_pin);
            actuation_on[valve_pin] = true;
            break;
        case OPEN_VENT:
            open(valve_pin);
            actuation_on[valve_pin] = true;
            break;
        case PULSE:
            pulse(valve_pin);
            actuation_on[valve_pin] = true;
            break;
        }
    }
}

void ValveArduino::sendData() {
    unsigned long data = 0;
    if (override) {
        data = 1;
    }
    for (int valve = 0; valve < NUM_VALVES; valve++) {
        int state = states[ALL_PINS[valve]];
        if (!actuation_on[ALL_PINS[valve]]) {
            state = 0;
        }
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

void ValveArduino::actuate(int loc_idx, int actuation_idx) {
    int valve_pin = VALVE_ORDER[loc_idx];
    switch (actuation_idx) {
    case 0:
        // Pulse
        pulse(valve_pin);
        break;
    case 1:
        // Open vent
        open(valve_pin);
        break;
    case 2:
        // Close vent
        close(valve_pin);
        break;
    case 3:
        // None
        // TODO: Implement this
        break;
    default:
        error();
        break;
    }
}

void ValveArduino::pi() {
    // TODO: implement this
}