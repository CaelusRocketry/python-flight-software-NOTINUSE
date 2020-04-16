#ifndef FLIGHT_TELEMETRYTASK_HPP
#define FLIGHT_TELEMETRYTASK_HPP

#include <string>
#include <flight/modules/drivers/Telemetry.hpp>

using namespace std;

class TelemetryTask {
private:
    Telemetry* telemetry;

public:
    TelemetryTask();
    void read();
    void actuate();
};


#endif //FLIGHT_TELEMETRYTASK_HPP
