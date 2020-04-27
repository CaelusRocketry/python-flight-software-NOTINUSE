#ifndef FLIGHT_REGISTRY_HPP
#define FLIGHT_REGISTRY_HPP

#include <iostream>
#include <assert.h>
#include <string>
#include <unordered_map>
#include <flight/modules/mcl/Field.hpp>
#include <flight/modules/mcl/FieldBase.hpp>
#include <Logger/logger_util.h>

using namespace std;

class Registry {
private:
    unordered_map<string, FieldBase *> fields;

    template <typename T>
    Field<T>* cast(FieldBase* base){
        Field<T>* field = dynamic_cast<Field<T>*>(base);
        if(field){
            return field;
        }
        log("Dynamic casting failed");
        return nullptr;
    }

public:
    Registry();

    template <typename T>
    void add(string path, T value){
        fields[path] = new Field<T>(path, value);
    }

    template <typename T>
    void add(string path){
        fields[path] = new Field<T>(path);
    }

    template <typename T>
    T get(string path){
        assert(fields.find(path) != fields.end());
        //log("Field exists");
        Field<T>* field = cast<T>(fields[path]);
        if(field){
            T val = field->getVal();
            return val;
        }
        log("Dynamic casting no work");
        // TODO: Can't assert in the final version, need to somehow return an error?
        assert(false);
        T val = field->getVal();
        return val;
//        return NULL;
    }


    template <typename T>
    bool put(string path, T value){
        Field<T>* field = cast<T>(fields[path]);
        if(field){
            field->setVal(value);
            return true;
        }
        assert(false);
        return false;
    }
};

#endif //FLIGHT_REGISTRY_HPP

