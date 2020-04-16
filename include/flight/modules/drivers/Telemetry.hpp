#ifndef FLIGHT_TELEMETRY_HPP
#define FLIGHT_TELEMETRY_HPP

#include <string>

using namespace std;

class Telemetry {
private:
    string IP;
    int port;

public:
    Telemetry();
    string read();
    void write();
};


#endif //FLIGHT_TELEMETRY_HPP
