#include <Solenoid.hpp>

Solenoid::Solenoid(int pin, bool special, bool no) {
    this->pin = pin;
    this->isSpecial = special;
    this->isNO = no;
    this->last_actuation_time = 0;
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

    this->last_actuation_time = getTime();

    if(this->isSpecial) {
        this->isOpen = true;
        std::thread controlThread(&Solenoid::controlOpen(), this);
        controlThread.detach();
    }
}

void Solenoid::pulse() {
    if(this->isNO) {
        digitalWrite(this->pin, LOW);
    }
    else {
        digitalWrite(this->pin, HIGH);
    }

    std::this_thread::sleep_for(std::chrono::seconds(0.5));

    if(this->isNO) {
        digitalWrite(this->pin, HIGH);
    }
    else {
        digitalWrite(this->pin, LOW);
    }

    this->isOpen = false;
}

void Solenoid::controlOpen() {
    while(this->isOpen) {
        if(this->getTime() - this->last_actuation_time >= this->MAX_SPECIAL_OPEN) {
            // relieveSpecial prevents the solenoid from being closed from the other thread while this thread is asleep
            // TODO: check if this actually works bc idk if mutex locks digitalWrite along with the other class resources

            this->mtx.lock();
            relieveSpecial();
            this->mtx.unlock();
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(20))
    }
}

unsigned long Solenoid::getTime() {
    unsigned long time = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
    return time;
}

void Solenoid::relieveSpecial() {
    // close solenoid temporarily

    if(this->isNO) {
        digitalWrite(this->pin, HIGH);
    }
    else {
        digitalWrite(this->pin, LOW);
    }

    std::this_thread::sleep_for(std::chrono::seconds(1))

    // open solenoid

    if(this->isNO) {
        digitalWrite(this->pin, LOW);
    }
    else {
        digitalWrite(this->pin, HIGH);
    }

    this->last_actuation_time = getTime();
    this->isOpen = true;
}

bool Solenoid::getStatus() {
    mtx.lock();
    bool ret = this->isOpen;
    mtx.unlock();
    return ret;
}