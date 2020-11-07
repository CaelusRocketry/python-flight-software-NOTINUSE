#include "Arduino.h"
#include "Constants.hpp"

#ifndef SOLENOID_HPP
#define SOLENOID_HPP

class Solenoid {
    private:  
        int openSignal;
        int closeSignal;
        int currSignal;

        unsigned long lastActuationTime;
        bool beingRelieved;

        void close();
        void open();
        void pulse();
        void setLow();
        void setHigh();

        void controlPulse();
        void controlSpecial();

    public:
        int pin;
        bool isSpecial;
        bool isNO;
        bool overridden;

        int actuation;
        Solenoid();
        Solenoid(int pin, bool special, bool no);
        void actuate(int actuationType);
        void control();
        void printSomething();
        int getState();
        int getActuation();
        void error(String error);
};

#endif
