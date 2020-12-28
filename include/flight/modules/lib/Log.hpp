#ifndef FLIGHT_LOG_HPP
#define FLIGHT_LOG_HPP

#include <string>
#include <vector>
#include <chrono>
#include <nlohmann/json.hpp>

using namespace std;
using nlohmann::json;

class Log;

void to_json(json& j, const Log& log);
void from_json(const json& j, Log& log);

// Log class stores messages to be sent to and from ground and flight station
class Log {
private:
    string header;
    json message;
    long timestamp;

public:
    Log() = default;

    Log(const string& header, const json& message, long timestamp = std::chrono::system_clock::now().time_since_epoch().count(), bool save = true)
        : header(header),
          message(message),
          timestamp(timestamp) {
        if (save) {
            this->save();
        }
    }

    void save(const string& filename = "black_box.txt") const;
    Log copy();
    string getHeader() const;
    json getMessage() const;
    long getTimestamp() const;
};


#endif //FLIGHT_LOG_HPP
