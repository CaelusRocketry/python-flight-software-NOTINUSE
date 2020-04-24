//
// Created by AC on 4/24/2020.
//

#ifndef FLIGHT_PACKET_HPP
#define FLIGHT_PACKET_HPP

#include <string>
#include <vector>

// Level Enum indicates the priority or status of the Packet
enum class LogPriority {
    INFO = 4,
    DEBUG = 3,
    WARN = 2,
    CRIT = 1
};

// Log class stores messages to be sent to and from ground and flight station
class Log {
private:
    std::string header;
    std::string message;
    double timestamp;
    bool save;

public:
    void save(std::string filename = "black_box.txt");
    std::string toString();
    Log copy();
    static Log fromString(std::string inputString);

};

// Packet class groups together logs of similar priority
class Packet {
private:
    std::vector<std::string> logs;
    double timestamp;
    LogPriority level;

public:
    void add(Log log);
    std::string toString();
    static Packet fromString(std::string inputString);
    bool operator<(const Packet& packet) const;

};

#endif //FLIGHT_PACKET_HPP
