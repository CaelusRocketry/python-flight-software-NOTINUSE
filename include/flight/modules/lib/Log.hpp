#ifndef FLIGHT_LOG_HPP
#define FLIGHT_LOG_HPP

#include <string>
#include <vector>
#include <chrono>

using namespace std;

// Log class stores messages to be sent to and from ground and flight station
class Log {
private:
    string header;
    string message;
    long timestamp;

public:
    Log(const string& header, const string& message, long timestamp = std::chrono::system_clock::now().time_since_epoch().count(), bool save = true)
        : header(header),
          message(message),
          timestamp(timestamp) {
        if (save) {
            this->save();
        }
    }

    void save(string filename = "black_box.txt");
    string toString() const;
    Log copy();
    static Log fromString(string inputString);
    string getHeader();
    string getMessage();
};


#endif //FLIGHT_LOG_HPP
