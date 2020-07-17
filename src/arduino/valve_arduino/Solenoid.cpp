#include <Solenoid.hpp>

Solenoid::Solenoid(int pin, bool special, bool no) {
    this->pin = pin;
    this->isSpecial = special;
    this->isNO = no;
    this->last_actuation_time = 0;
    this->isOpen = false;
    this->isPulse = false;
    this->beingRelieved = false;
}

void Solenoid::close() {
    if(this->isNO) {
        digitalWrite(this->pin, HIGH);
    }
    else {
        digitalWrite(this->pin, LOW);
    }
    this->isOpen = false;
}

void Solenoid::open() {
    if(this->isNO) {
        digitalWrite(this->pin, LOW);
    }
    else {
        digitalWrite(this->pin, HIGH);
    }

    this->last_actuation_time = millis();
    this->isOpen = true;
}

void Solenoid::pulse() {
    this->isPulse = true;

    if(this->isNO) {
        digitalWrite(this->pin, LOW);
    }
    else {
        digitalWrite(this->pin, HIGH);
    }

    this->last_actuation_time = millis();
}

void Solenoid::controlPulse() {
    if(millis() - this->last_actuation_time >= 500) {
        if(this->isNO) {
            digitalWrite(this->pin, HIGH);
        }
        else {
            digitalWrite(this->pin, LOW);
        }

        this->isPulse = false;
        this->last_actuation_time = millis();
    }
}

bool Solenoid::getPulse() {
    return this->isPulse;
}

void Solenoid::controlOpen() {
    if(millis() - this->last_actuation_time >= this->MAX_SPECIAL_OPEN) {
        relieveSpecial();
    }
    else if(this->beingRelieved) {
        reOpenSpecial();
    }
}

void Solenoid::relieveSpecial() {
    // close solenoid temporarily

    if(this->isNO) {
        digitalWrite(this->pin, HIGH);
    }
    else {
        digitalWrite(this->pin, LOW);
    }

    this->last_actuation_time = millis();
    this->beingRelieved = true;
}

void Solenoid::reOpenSpecial() {
    // open solenoid

    if((millis() - this->last_actuation_time >= this->RELIEF_WAIT_TIME) && this->isOpen) {
        if(this->isNO) {
            digitalWrite(this->pin, LOW);
        }
        else {
            digitalWrite(this->pin, HIGH);
        }

        this->last_actuation_time = millis();
        this->beingRelieved = false;
    }
    else if(!this->isOpen) {
        this->beingRelieved = false;
    }
}

bool Solenoid::getStatus() {
    return this->isOpen;
}

bool Solenoid::getSpecial() {
    return this->isSpecial;
}