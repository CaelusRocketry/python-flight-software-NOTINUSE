#include <Logger/logger_util.h>
#include <flight/modules/tasks/SensorTask.hpp>
#include <flight/modules/lib/Util.hpp>

void SensorTask::initialize(){

    // Generates the sensor list
    for(string outer : Util::parse_json({"sensors", "list"})) {
        for(string inner : Util::parse_json_list({"sensors", "list", outer})) {
            sensor_list.push_back(make_tuple(outer, inner));
            // NUM_SENSORS += 1;
        }
    }

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

        // sensor type, i.e thermocouple, pressure, etc.
        string type = get<0>(sensor);
        // specific sensor, pressure sensor 1, pressure sensor 2, etc.
        string loc = get<1>(sensor);
        string path = "sensor_measured." + type + "." + loc;
        registry->put<double>(path, value);
    }
}

void SensorTask::actuate(){
    return;
}