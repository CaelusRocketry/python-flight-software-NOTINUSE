#include <iostream>
#include <fstream>
#include <flight/modules/lib/Log.hpp>

using nlohmann::json;

void to_json(json& j, const Log& log) {
    j = json{
        {"header", log.getHeader()},
        {"message", log.getMessage()},
        {"timestamp", log.getTimestamp()}
    };
}

void from_json(const json& j, Log& log) {
    string header, message;
    long timestamp;
    j.at("header").get_to(header);
    j.at("message").get_to(message);
    j.at("timestamp").get_to(timestamp);
    log = Log(header, message, timestamp);
}

// Log string to black_box.txt
void Log::save(const string& filename) const {
    ofstream file;
    file.open(filename, fstream::in | fstream::out | fstream::app);

    if(!file) {
        file.open(filename, fstream::in | fstream::out | fstream::trunc);
    }

    json j;
    to_json(j, *this);

    file << j.dump() << endl;
    file.close();
}

Log Log::copy(){
    // Create a copy of the log
    return Log(header, message, timestamp, false);
}

string Log::getHeader() const {
    return header;
}

json Log::getMessage() const {
    return message;
}

long Log::getTimestamp() const {
    return timestamp;
}