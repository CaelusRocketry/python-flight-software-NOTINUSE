//
// Created by adiv413 on 6/25/2020.
//

#include <flight/modules/control_tasks/Control.hpp>
#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Flag.hpp>
#include <flight/modules/lib/Log.hpp>

#ifndef FLIGHT_PRESSURECONTROL_HPP
#define FLIGHT_PRESSURECONTROL_HPP

class PressureControl : public Control {
private:
    Registry *registry;
    Flag *flag;
    void check_pressure();

public:
    PressureControl(Registry *registry, Flag *flag);
    void begin();
    void execute();
};
#endif //FLIGHT_PRESSURECONTROL_HPP
