//
// Created by AC on 4/24/2020.
//

#ifndef FLIGHT_PACKET_HPP
#define FLIGHT_PACKET_HPP

#include <string>
#include <vector>
#include <chrono>
#include <flight/modules/lib/Enums.hpp>
#include <flight/modules/lib/Log.hpp>

using namespace std;

// Packet class groups together logs of similar priority
class Packet {
private:
    vector<Log> logs;
    long timestamp;
    LogPriority level;

public:
    Packet(LogPriority l, long t = std::chrono::system_clock::now().time_since_epoch().count())
            : level(l),
              timestamp(t){}

    void add(Log log);
    string toString();
    static Packet fromString(string inputString);
    vector<Log> getLogs();

    struct compareTo {
        bool operator()(Packet lhs, Packet rhs)
        {
            if(lhs.level != rhs.level) {
                return lhs.level < rhs.level;
            }
            return lhs.timestamp < rhs.timestamp;
        }
    };

};

#endif //FLIGHT_PACKET_HPP
