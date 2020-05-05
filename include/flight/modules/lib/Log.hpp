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
    Log(string h, string m, long t = std::chrono::system_clock::now().time_since_epoch().count(), bool save = true)
            : header(h),
              message(m),
              timestamp(t) {
        if(save){
            this->save();
        }
    }
    void save(string filename = "black_box.txt");
    string toString();
    Log copy();
    static Log fromString(string inputString);
    string getHeader();
    string getMessage();
};


#endif //FLIGHT_LOG_HPP
