#include <Arduino.h>
#include <thread>
#include <chrono>
#include <atomic>
#include <mutex>

#ifndef SOLENOID_HPP
#define SOLENOID_HPP

class Solenoid {
    private:
        int pin;
        bool isSpecial;
        bool isNO;
        unsigned long last_actuation_time;

        std::mutex mtx;
        std::atomic<bool> isOpen{false};
        const unsigned long MAX_SPECIAL_OPEN = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::seconds(4)).count();

        unsigned long getTime();
        void controlOpen();
        void relieveSpecial();

    public:
        Solenoid(int pin, bool special, bool no);
        void close();
        void open();
        void pulse();
        bool getStatus();
};

#endif