#ifndef FLIGHT_TELEMETRYTASK_HPP
#define FLIGHT_TELEMETRYTASK_HPP

#include <string>
#include <flight/modules/tasks/Task.hpp>
#include <flight/modules/drivers/Telemetry.hpp>

class TelemetryTask : public Task {
private:
    Telemetry* _telemetry;

public:
    TelemetryTask(Registry* r, Flag* f)
    : Task(r, f) {}
    void initialize();
    void read();
    void actuate();
};


#endif //FLIGHT_TELEMETRYTASK_HPP
