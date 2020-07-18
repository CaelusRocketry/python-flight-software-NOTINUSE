#include "Arduino.h"

#ifndef SOLENOID_HPP
#define SOLENOID_HPP

class Solenoid {
    private:  
        int openSignal;
        int closeSignal;
        int currSignal;

        unsigned long lastActuationTime;
        bool beingRelieved;
        
        const int NO_ACTUATION = 0;
        const int CLOSE_VENT = 1;
        const int OPEN_VENT = 2;
        const int PULSE = 3;

        const unsigned long MAX_SPECIAL_POWER = 4000;
        const unsigned long RELIEF_WAIT_TIME = 1000;
        const unsigned long PULSE_TIME = 500;

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

        int actuation;

        Solenoid(int pin, bool special, bool no);
        void actuate(int actuationType);
        void control();
        int getStatus();
};

#endif