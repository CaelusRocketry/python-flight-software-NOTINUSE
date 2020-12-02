#include <Logger/logger_util.h>
#include <flight/modules/tasks/SensorTask.hpp>

void SensorTask::initialize(){
    sensor_list.push_back(make_tuple("thermocouple", "chamber"));
    sensor_list.push_back(make_tuple("thermocouple", "tank"));
    sensor_list.push_back(make_tuple("pressure", "chamber"));
    sensor_list.push_back(make_tuple("pressure", "injector"));
    sensor_list.push_back(make_tuple("pressure", "tank"));
    sensor_list.push_back(make_tuple("load", "tank"));

    sensor = new Arduino("PseudoSensor");
    log("Sensor task started");
}

void SensorTask::read(){
    char* data = sensor->read(); // data returned as an array of chars

    // Convert char array to double array
    union Conversion {
        double values[NUM_SENSORS];
        char bytes[NUM_SENSORS * sizeof(double)];
    };
    Conversion conv;
    for(int i = 0; i < NUM_SENSORS * sizeof(double); i++){
        conv.bytes[i] = data[i];
    }

    double* values = conv.values;

    // Update registry
    for(int i = 0; i < NUM_SENSORS; i++){
        auto sensor = sensor_list[i];
        double value = values[i];
        string type = get<0>(sensor);
        string loc = get<1>(sensor);
        registry->put<double>("sensor_measured." + type + "." + loc, value);
    }
}

void SensorTask::actuate(){
    return;
}