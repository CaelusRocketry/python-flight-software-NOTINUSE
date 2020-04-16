#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Field.hpp>
#include <Logger/logger_util.h>

Registry::Registry(){
    log("Registry created");

    // Sensor fields

    // Valve fields

    // Telemetry fields

    // General fields
    add<bool>("general.hard_abort", false);
    add<bool>("general.soft_abort", false);
    put<int>("general.stage", 0);
    add<int>("general.stage_progress", 0);
}

template <typename T>
void Registry::add(string path, T value){
    fields[path] = new Field<T>(path, value);
}

template <typename T>
T Registry::get(string path){
    Field<T>* field = cast<T>(fields[path]);
    if(field){
        return field->getVal();
    }
    return nullptr;
}

template <typename T>
void Registry::put(string path, T value){
    fields[path] = new Field<T>(path, value);
}

/*
template <typename T>
void Registry::put(string path, T value){
    Field<T>* field = cast<T>(fields[path]);
    if(field){
        field->setVal(value);
//        return true;
    }
//    return false;
}
*/

//template <typename T>
//void Registry::put(string path, T value){
//    fields[path] = new Field<T>(path, value);
//}


template <typename T>
Field<T>* Registry::cast(FieldBase* base){
    Field<T>* field = dynamic_cast<Field<T>*>(base);
    if(field){
        return field;
    }
    log("Dynamic casting failed");
    return nullptr;
}