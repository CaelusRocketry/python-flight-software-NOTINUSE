#include <flight/modules/lib/Util.hpp>

vector<string> Util::split(const string &s, const string &delimiter){
    vector<string> result;
    int start = 0;
    int end = 0;
    while (end != string::npos) {
        end = s.find(delimiter, start);
        result.push_back(s.substr(start, end-start));
        start = end + delimiter.length();
    }
    return result;
}
