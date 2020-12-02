#include <iostream>
#include <fstream>
#include <map>
#include <flight/modules/lib/Log.hpp>
#include <flight/modules/lib/Util.hpp>

// Log string to black_box.txt
void Log::save(string filename){
    ofstream file;
    file.open(filename, fstream::in | fstream::out | fstream::app);
    if(!file){
        file.open(filename,  fstream::in | fstream::out | fstream::trunc);
    }
    file << toString() << endl;
    file.close();
}

string Log::toString() {
    // Create map representing Log object data
    map<string, string> my_data;
    my_data.insert(pair<string, string>("header", header));
    my_data.insert(pair<string, string>("message", message));
    my_data.insert(pair<string, string>("timestamp", to_string(timestamp)));
    return Util::map_to_string(my_data, ":", ",");
}

Log Log::copy(){
    // Create a copy of the log
    return Log(header, message, timestamp, false);
}

Log Log::fromString(string inputString){
    // Convert input string to map with Log object data and create Log
    map<string, string> data = Util::string_to_map(inputString, ":", ",");
    return Log(data["header"], data["message"], stol(data["timestamp"]));
}

string Log::getHeader() {
    return this->header;
}

string Log::getMessage() {
    return this->message;
}