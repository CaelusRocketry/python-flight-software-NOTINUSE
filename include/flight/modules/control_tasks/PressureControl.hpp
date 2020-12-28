//
// Created by adiv413 on 6/25/2020.
//

#ifndef FLIGHT_PRESSURECONTROL_HPP
#define FLIGHT_PRESSURECONTROL_HPP

#include <flight/modules/control_tasks/Control.hpp>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>
#include <flight/modules/lib/Log.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <unordered_map>

class PressureControl : public Control {
private:
    Registry *registry;
    Flag *flag;
    const vector<pair<string, string>> matchups {
        {"PT-2", "pressure_relief"}
    };
    void check_pressure();

public:
    PressureControl() = default;
    void begin();
    void execute();
};
#endif //FLIGHT_PRESSURECONTROL_HPP
