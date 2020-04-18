#include <Logger/logger_util.h>
#include <flight/modules/drivers/PseudoSensor.hpp>

PseudoSensor::PseudoSensor(){
    // List all sensors (this should normally be done in a config.json)
    sensor_list.push_back(make_tuple("thermocouple", "chamber"));
    sensor_list.push_back(make_tuple("thermocouple", "tank"));
    sensor_list.push_back(make_tuple("pressure", "chamber"));
    sensor_list.push_back(make_tuple("pressure", "injector"));
    sensor_list.push_back(make_tuple("pressure", "tank"));
    sensor_list.push_back(make_tuple("load", "tank"));

    // Initialize sensor values to be random
    for(auto tup : sensor_list){
        sensor_values[tup] = rand() % 100 + 100;
    }
}

void PseudoSensor::set_sensor_values(){
    for(auto tup : sensor_list){
        sensor_values[tup] = sensor_values[tup] + (rand() % 20 - 10);
    }
}

char* PseudoSensor::read(){
    set_sensor_values();
    union Conversion {
        double values[NUM_SENSORS];
        char bytes[NUM_SENSORS * sizeof(double)];
    };
    Conversion conv;
    static char bytes[NUM_SENSORS * 4];
    for(int i = 0; i < NUM_SENSORS; i++){
        auto tup = sensor_list[i];
        double val = sensor_values[tup];
        conv.values[i] = val;
    }
    static char ret[NUM_SENSORS * sizeof(double)];
    for(int i = 0; i < NUM_SENSORS * sizeof(double); i++){
        ret[i] = conv.bytes[i];
    }
    return ret;
}

void PseudoSensor::write(char* msg){
    // Sensor has nothing to write
}