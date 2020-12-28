#ifndef FLIGHT_UTIL_HPP
#define FLIGHT_UTIL_HPP

#include <iostream>
#include <vector>
#include <map>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <Logger/logger_util.h>
#include <flight/modules/mcl/Flag.hpp>
#include <flight/modules/lib/Log.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <flight/modules/lib/Packet.hpp>
#include <flight/modules/lib/Errors.hpp>

using namespace std;

namespace Util {
    /** Split a string by a delimiter */
    vector<string> split(const string &s, const string &delimiter);
}

#endif // FLIGHT_UTIL_HPP