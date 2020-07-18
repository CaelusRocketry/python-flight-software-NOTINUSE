#include <Solenoid.hpp>

Solenoid::Solenoid(int pin, bool special, bool no) {
    this->pin = pin;
    this->isSpecial = special;
    this->isNO = no;
    if(no){
        this->openSignal = LOW;
        this->closeSignal = HIGH;
    }
    else{
        this->openSignal = HIGH;
        this->closeSignal = LOW;
    }
    this->lastActuationTime = 0;
    this->beingRelieved = false;
    this->actuation = NO_ACTUATION;
    pinMode(this->pin, OUTPUT);
    setLow();
}

void Solenoid::close() {
    digitalWrite(pin, closeSignal);
    this->currSignal = closeSignal;
    this->actuation = this->CLOSE_VENT;
    this->lastActuationTime = millis();
}

void Solenoid::open() {
    digitalWrite(pin, openSignal);
    this->currSignal = openSignal;
    this->actuation = this->OPEN_VENT;
    this->lastActuationTime = millis();
}

void Solenoid::pulse() {
    digitalWrite(pin, openSignal);
    this->currSignal = openSignal;
    this->actuation = this->PULSE;
    this->lastActuationTime = millis();
}

void Solenoid::setLow() {
    if(closeSignal == LOW){
        close();
    }
    else{
        open();
    }
}

void Solenoid::setHigh() {
    if(closeSignal == HIGH){
        close();
    }
    else{
        open();
    }
}

void Solenoid::control(){
    controlPulse();
    controlSpecial();
}

void Solenoid::controlPulse() {
    if(!this->actuation == PULSE){ // Ignore this method if it's not pulsing
        return;
    }
    if(millis() - this->lastActuationTime >= PULSE_TIME) {
        close();
        this->actuation = NO_ACTUATION;
    }
}

void Solenoid::controlSpecial() {
    if(!this->isSpecial){ // This method only applies to "special" valves
        return;
    }
    if(this->currSignal == HIGH){ // If it's currently using power to actuate...
        if(millis() - this->lastActuationTime >= MAX_SPECIAL_POWER){
            setLow(); // Relieve the valve
            this->beingRelieved = true;
        }
    }
    else if(this->beingRelieved) {
        if(millis() - this->lastActuationTime >= RELIEF_WAIT_TIME){
            setHigh();
            this->beingRelieved = false;
        }
    }
}

void Solenoid::actuate(int actuationType){
    switch (actuationType) {
        case NO_ACTUATION:
            break;
        case CLOSE_VENT:
            close();
            break;
        case OPEN_VENT:
            open();
            break;
        case PULSE:
            pulse();
            break;
        default:
            error("Unknown actuation type");
            break;
    }
    this->actuation = actuationType;
}

int Solenoid::getState(){
    // Returns 1 if open, 0 if closed
    if(currSignal == openSignal){
        return 1;
    }
    return 0;
}