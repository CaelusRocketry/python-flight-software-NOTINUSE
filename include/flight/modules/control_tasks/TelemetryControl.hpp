//
// Created by Srikar on 4/15/2020.
//

#include <flight/modules/control_tasks/Control.hpp>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>

#ifndef FLIGHT_TELEMETRYCONTROL_HPP
#define FLIGHT_TELEMETRYCONTROL_HPP

class TelemetryControl : public Control {
private:
    Registry *registry;
    Flag *flag;

    void ingest();
    void heartbeat();
    void hard_abort();
    void soft_abort();
    void solenoid_actuate();
    void sensor_request();
    void valve_request();
    void progress();
    void test();

public:
    TelemetryControl(Registry *registry, Flag *flag);
    void begin();
    void execute();
};
#endif //FLIGHT_TELEMETRYCONTROL_HPP
