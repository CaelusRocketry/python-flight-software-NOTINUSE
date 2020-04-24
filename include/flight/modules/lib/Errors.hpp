//
// Created by AC on 4/24/2020.
//

#ifndef FLIGHT_ERRORS_HPP
#define FLIGHT_ERRORS_HPP

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

#endif //FLIGHT_ERRORS_HPP
