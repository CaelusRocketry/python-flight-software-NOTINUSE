//
// Created by Srikar on 4/15/2020.
//

#include <flight/modules/control_tasks/Control.hpp>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>
#include <flight/modules/lib/Log.hpp>

#ifndef FLIGHT_TELEMETRYCONTROL_HPP
#define FLIGHT_TELEMETRYCONTROL_HPP

class TelemetryControl : public Control {

typedef void (TelemetryControl::*functionType)(vector<string>);

private:
    Registry *registry;
    Flag *flag;
    unordered_map<string, functionType> functions;
    const unordered_map<string, vector<string>> arguments {
            {"heartbeat", {}},
            {"hard_abort", {}},
            {"soft_abort", {}},
            {"solenoid_actuate", {"valve_location", "actuation_type", "priority"}},
            {"sensor_request", {"sensor_type", "sensor_location"}},
            {"valve_request", {"valve_type", "valve_location"}},
            {"progress", {}},
            {"test", {"response"}}
        };

    void ingest(Log log);
    void heartbeat(vector<string> args);
    void hard_abort(vector<string> args);
    void soft_abort(vector<string> args);
    void solenoid_actuate(vector<string> args);
    void sensor_request(vector<string> args);
    void valve_request(vector<string> args);
    void progress(vector<string> args);
    void test(vector<string> args);
    void makeFunctions();

public:
    TelemetryControl(Registry *registry, Flag *flag);
    void begin();
    void execute();
};
#endif //FLIGHT_TELEMETRYCONTROL_HPP
