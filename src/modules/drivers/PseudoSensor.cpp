#include <Logger/logger_util.h>
#include <flight/modules/drivers/PseudoSensor.hpp>

PseudoSensor::PseudoSensor(){
    // List all sensors (this should normally be done in a config.json)
    sensor_list = {
        {"thermocouple", "chamber"},
        {"thermocouple", "tank"},
        {"pressure", "chamber"},
        {"pressure", "injector"},
        {"pressure", "tank"},
        {"load", "tank"}
    };

    // Initialize sensor values to be random
    for (const auto& sensor_ : sensor_list) {
        sensor_values[sensor_] = rand() % 100 + 100;
    }
}

void PseudoSensor::set_sensor_values() {
    // Adjust by a random value
    for (const auto& sensor_ : sensor_list) {
        sensor_values[sensor_] += (rand() % 20 - 10);
    }
}

/*
 * Convert double sensor values to char* and return
 */

unsigned char* PseudoSensor::read() {
    set_sensor_values();
    union {
        double values[NUM_SENSORS];
        char bytes[NUM_SENSORS * sizeof(double)];
    } conv;
    static unsigned char bytes[NUM_SENSORS * 4];
    for (int i = 0; i < NUM_SENSORS; i++) {
        auto tup = sensor_list[i];
        double val = sensor_values[tup];
        conv.values[i] = val;
    }
    static unsigned char ret[NUM_SENSORS * sizeof(double)];
    for (int i = 0; i < NUM_SENSORS * sizeof(double); i++) {
        ret[i] = conv.bytes[i];
    }
    return ret;
}

void PseudoSensor::write(unsigned char* msg){
    // Sensor has nothing to write
}