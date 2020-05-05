//
// Created by AC on 4/24/2020.
//

#ifndef FLIGHT_ERRORS_HPP
#define FLIGHT_ERRORS_HPP

#include <exception>

enum class Error {
    // no error
    NONE,

    // invalid packets
    INVALID_HEADER_ERROR,
    INVALID_ARGUMENT_ERROR,

    // invalid access attempt
    KEY_ERROR,

    // valve and sensor request errors
    REQUEST_ERROR,
    PRIORITY_ERROR,

    TELEM_CONNECTION_ERROR
};

class DYNAMIC_CAST_ERROR : public std::exception {
    virtual const char* what() const throw()
    {
        return "Dynamic casting doesn't work";
    }
};

#endif //FLIGHT_ERRORS_HPP
