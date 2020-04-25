//
// Created by adiv413 on 4/24/2020.
//

#ifndef FLIGHT_CONTROL_HPP
#define FLIGHT_CONTROL_HPP

class Control {
public:
    virtual void begin() = 0;
    virtual void execute() = 0;
};

#endif //FLIGHT_CONTROL_HPP
