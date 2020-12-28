#include <Logger/logger_util.h>
#include <flight/modules/drivers/Arduino.hpp>
#include <flight/modules/drivers/PseudoSensor.hpp>
#include <flight/modules/drivers/PseudoValve.hpp>

void Arduino::reset(){
    if (name == "PseudoSensor"){
        arduino = new PseudoSensor();
    } else if(name == "PseudoValve") {
        arduino = new PseudoValve();
    } else {
        log("REEEE UNKNOWN ARDUINO TYPE");
    }
}

unsigned char* Arduino::read() {
    return arduino->read();
}

void Arduino::write(unsigned char* msg) {
    arduino->write(msg);
}
