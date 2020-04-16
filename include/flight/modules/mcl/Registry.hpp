#ifndef FLIGHT_REGISTRY_HPP
#define FLIGHT_REGISTRY_HPP

#include <string>
#include <unordered_map>
#include <flight/modules/mcl/Field.hpp>
#include <flight/modules/mcl/FieldBase.hpp>
using namespace std;

class Registry {
private:
    unordered_map<string, FieldBase *> fields;

    template<typename T>
    Field<T> *cast(FieldBase *base);

public:
    Registry();

    template<typename T>
    void put(string path, T value);

    template<typename T>
    void add(string path, T value);

    template<typename T>
    T get(string path);

    // Returns true if the put worked else False
//    template <typename T>
//    void put(string path, T value);
};

#endif //FLIGHT_REGISTRY_HPP

