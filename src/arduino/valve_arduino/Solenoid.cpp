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
    this->overridden = false;
    pinMode(this->pin, OUTPUT);
    setLow();
}

void Solenoid::close() {
    // Serial.println("Closing");
    // Serial.println(closeSignal);
    digitalWrite(pin, closeSignal);
    this->currSignal = closeSignal;
    this->lastActuationTime = millis();
    this->beingRelieved = false;
}

void Solenoid::open() {
    digitalWrite(pin, openSignal);
    this->currSignal = openSignal;
    this->lastActuationTime = millis();
    this->beingRelieved = false;
}

void Solenoid::pulse() {
    digitalWrite(pin, openSignal);
    this->currSignal = openSignal;
    this->lastActuationTime = millis();
    Serial.println("Yam pulsing");
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
  Serial.println(this->actuation);
//    controlPulse();
//    controlSpecial();
}

void Solenoid::controlPulse() {
    if(this->actuation != PULSE){ // Ignore this method if it's not pulsing
        return;
    }
    Serial.println("PULSING");
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
    Serial.println("ACTUATING");
    Serial.println(this->actuation);
    printSomething();
    Serial.println("ACTUATING");
}

void Solenoid::printSomething(){
  Serial.println(this->actuation);
}

int Solenoid::getState(){
    // Returns 1 if open, 0 if closed
    if(currSignal == openSignal){
        return 1;
    }
    return 0;
}

int Solenoid::getActuation(){
    return actuation;
}

void Solenoid::error(String msg){
    digitalWrite(13, HIGH);
    // Serial.println(msg);
}
