#ifndef FLIGHT_FLAG_HPP
#define FLIGHT_FLAG_HPP

#include <iostream>
#include <assert.h>
#include <string>
#include <unordered_map>
#include <flight/modules/mcl/Field.hpp>
#include <flight/modules/mcl/FieldBase.hpp>
#include <Logger/logger_util.h>
#include <flight/modules/lib/Errors.hpp>

using namespace std;

class Flag {
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
    Flag();

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
        throw DYNAMIC_CAST_ERROR();
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

#endif //FLIGHT_FLAG_HPP

