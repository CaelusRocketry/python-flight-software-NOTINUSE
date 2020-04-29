#include <iostream>
#include <vector>
#include <map>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <Logger/logger_util.h>

using namespace std;

class Util {
public:

    /*
     * @param args: contains the path to the items you want to extract from config.json.
     * For example, if you want to get all of the sensor names, the method would be used
     * as parse_json({"sensors", "list"}).
     *
     * This method doesn't work if you're trying to parse from a list in config.json (like
     * if you're trying to get the locations of the sensors). If you want that functionality,
     * use parse_json_list instead.
    */

    static vector<string> parse_json(initializer_list<string> args);

    /*
     * Example: to get a list of all the solenoids, do parse_json_list({"valves", "list", "solenoid"}).
     * Note that you have to specify the field "solenoid" in order to get the items from the list.
     */

    static vector<string> parse_json_list(initializer_list<string> args);

    /*
     * Example: to get the value of telemetry's delay, do parse_json_value({"telemetry", "DELAY"}).
     * Note that you have to specify the field "DELAY" in order to get the items from the list.
     */

    static string parse_json_value(initializer_list<string> args);

    /*
     * Used to convert a dictionary (with string key and value) to a string.
     * Used by Log and Packet in the toString methods.
     * key_delim is the separator between the key and the value (for example ':' when python prints a dictionary)
     * element_delim is the separator between multiple elements (for example ',' when python prints a dictionary)
     */
    static string map_to_string(map<string, string> data, string key_delim, string element_delim);


    /*
     * Used to convert a string to a dictionary (with string key and value).
     * Used by Log and Packet in the toString methods.
     * Follows the format of map_to_string
     */
    static map<string, string> string_to_map(string data, string key_delim, string element_delim);

};