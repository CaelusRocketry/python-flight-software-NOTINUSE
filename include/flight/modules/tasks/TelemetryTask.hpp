#ifndef FLIGHT_TELEMETRYTASK_HPP
#define FLIGHT_TELEMETRYTASK_HPP

#include <string>
#include <flight/modules/drivers/Telemetry.hpp>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>

using namespace std;

class TelemetryTask {
private:
    Telemetry* _telemetry;
    Registry* _registry;
    Flag* _flag;

public:
    TelemetryTask();
    TelemetryTask(Registry* registry, Flag* flag);
    void read();
    void actuate();
};


#endif //FLIGHT_TELEMETRYTASK_HPP
