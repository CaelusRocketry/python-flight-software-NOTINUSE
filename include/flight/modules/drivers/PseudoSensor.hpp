#ifndef FLIGHT_PSEUDOSENSOR_HPP
#define FLIGHT_PSEUDOSENSOR_HPP

#define NUM_SENSORS 6

#include <vector>
#include <string>
#include <map>
#include <flight/modules/drivers/PseudoArduino.hpp>

class PseudoSensor : public PseudoArduino {
private:
    vector<pair<string, string>> sensor_list;
    map<pair<string, string>, double> sensor_values;

    void set_sensor_values();

public:
    PseudoSensor();
    unsigned char* read() override;
    void write(unsigned char* msg) override;
};

#endif //FLIGHT_PSEUDOSENSOR_HPP
