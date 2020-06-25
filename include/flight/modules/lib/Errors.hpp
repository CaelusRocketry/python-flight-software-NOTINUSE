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

class PACKET_ARGUMENT_ERROR : public std::exception {
    virtual const char* what() const throw()
    {
        return "Invalid packet: number of arguments for the function specified in the GS packet doesn't match the number of arguments in the FS function definition.";
    }
};

class INVALID_HEADER_ERROR : public std::exception {
    virtual const char* what() const throw()
    {
        return "Invalid packet: GS packet header doesn't match any of the valid packet headers.";
    }
};

class INVALID_SOLENOID_ERROR : public std::exception {
    virtual const char* what() const throw()
    {
        return "Unable to find an actuatable solenoid.";
    }
};

class INSUFFICIENT_PRIORITY_SOLENOID_ERROR : public std::exception {
    virtual const char* what() const throw()
    {
        return "Too little priority to actuate solenoid.";
    }
};

class INVALID_PACKET_MESSAGE_ERROR : public std::exception {
    virtual const char* what() const throw()
    {
        return "Invalid GS packet message.";
    }
};

class INVALID_SENSOR_LOCATION_ERROR : public std::exception {
    virtual const char* what() const throw()
    {
        return "Invalid GS packet message: cannot find the specified sensor.";
    }
};

class INVALID_VALVE_LOCATION_ERROR : public std::exception {
    virtual const char* what() const throw()
    {
        return "Invalid GS packet message: cannot find the specified valve.";
    }
};

class SOCKET_READ_ERROR : public std::exception {
    virtual const char* what() const throw()
    {
        return "An unexpected error occurred while reading from the socket.";
    }
};

class SOCKET_CREATION_ERROR : public std::exception {
    virtual const char* what() const throw()
    {
        return "An unexpected error occurred while creating the socket.";
    }
};

class INVALID_ADDRESS_ERROR : public std::exception {
    virtual const char* what() const throw()
    {
        return "Invalid socket address/address not supported.";
    }
};

class SOCKET_CONNECTION_ERROR : public std::exception {
    virtual const char* what() const throw()
    {
        return "Socket connection failed.";
    }
};

class JSON_ARGUMENT_ERROR : public std::exception {
    virtual const char* what() const throw()
    {
        return "No arguments to parse json";
    }
};

class JSON_PARSE_ERROR : public std::exception {
    virtual const char* what() const throw()
    {
        return "An unexpected error occurred while parsing json";
    }
};

#endif //FLIGHT_ERRORS_HPP
