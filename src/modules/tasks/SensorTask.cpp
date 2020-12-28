#include <Logger/logger_util.h>
#include <flight/modules/tasks/SensorTask.hpp>
#include <flight/modules/mcl/Config.hpp>

void SensorTask::initialize() {
    // Generates the sensor list
    /* Pair of <string, <string, sensorinfo>> */
    for (const auto& type_ : global_config.sensors.list) {
        /* Pair of <string, sensorinfo> */
        for (const auto& location_ : type_.second) {
            sensor_list.push_back(make_pair(type_.first, location_.first));
        }
    }

    sensor = new Arduino("PseudoSensor");
    log("Sensor: Initialized");
}

void SensorTask::read() {
    log("Sensor: Reading");
    unsigned char *data = sensor->read(); // data returned as an array of chars

    // Convert char array to double array
    union {
        double values[NUM_SENSORS];
        unsigned char bytes[NUM_SENSORS * sizeof(double)];
    } conv;

    for (int i = 0; i < NUM_SENSORS * sizeof(double); i++) {
        conv.bytes[i] = data[i];
    }

    double *values = conv.values;

    // Update registry
    for (int i = 0; i < NUM_SENSORS; i++) {
        auto sensor_ = sensor_list[i];
        double value = values[i];

        // sensor type, i.e thermocouple, pressure, etc.
        string type = sensor_.first;
        // specific sensor, pressure sensor 1, pressure sensor 2, etc.
        string loc = sensor_.second;
        global_registry.sensors[type][loc].measured_value = value;
    }
}

void SensorTask::actuate() {}