#ifndef SOLENOID_HPP
#define SOLENOID_HPP

class Solenoid {
    private:
        int pin;
        bool isSpecial;
        bool isNO;
        unsigned long last_actuation_time;
        bool isOpen;
        bool beingRelieved;
        bool isPulse;
        int actuation;
        
        const int NO_ACTUATION = 0;
        const int CLOSE_VENT = 1;
        const int OPEN_VENT = 2;
        const int PULSE = 3;

        const unsigned long MAX_SPECIAL_OPEN = 4000;
        const unsigned long RELIEF_WAIT_TIME = 1000;

        void relieveSpecial();
        void reOpenSpecial();

    public:
        Solenoid(int pin, bool special, bool no);
        void close();
        void open();
        void pulse();
        bool getStatus();
        bool getSpecial();
        void controlOpen();
        bool getPulse();
        void controlPulse();
        int getActuation();
        int getPin();
};

#endif