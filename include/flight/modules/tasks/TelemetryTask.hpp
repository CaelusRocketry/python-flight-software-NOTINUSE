#ifndef FLIGHT_TELEMETRYTASK_HPP
#define FLIGHT_TELEMETRYTASK_HPP

#include <string>
#include <flight/modules/tasks/Task.hpp>
#include <flight/modules/drivers/Telemetry.hpp>

class TelemetryTask : public Task {
private:
    Telemetry telemetry;

public:
    TelemetryTask() {}
    void initialize();
    void read();
    void enqueue();
    void actuate();
};


#endif //FLIGHT_TELEMETRYTASK_HPP
