#include "Solenoid.hpp"

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
    this->actuation = CLOSE_VENT;
    this->lastActuationTime = millis();
}

void Solenoid::open() {
    digitalWrite(pin, openSignal);
    this->currSignal = openSignal;
    this->actuation = OPEN_VENT;
    this->lastActuationTime = millis();
}

void Solenoid::pulse() {
    digitalWrite(pin, openSignal);
    this->currSignal = openSignal;
    this->actuation = PULSE;
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
    if(millis() - this->lastActuationTime >= PULSE_WAIT_TIME) {
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
    if(actuationType == NO_ACTUATION){
        // Do nothing
    }
    else if(actuationType == CLOSE_VENT){
        close();
    }
    else if(actuationType == OPEN_VENT){
        open();
    }
    else if(actuationType == PULSE){
        pulse();
    }
    else{
        error("Unknown actuation type");
        return;
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

void Solenoid::error(String msg){
    digitalWrite(13, HIGH);
    Serial.println(msg);
}
