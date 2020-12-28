#ifndef FLIGHT_REGISTRY_HPP
#define FLIGHT_REGISTRY_HPP

#include <iostream>
#include <assert.h>
#include <string>
#include <map>
#include <queue>
#include <flight/modules/mcl/Field.hpp>
#include <flight/modules/lib/Enums.hpp>
#include <flight/modules/lib/Packet.hpp>
#include <flight/modules/mcl/FieldBase.hpp>
#include <Logger/logger_util.h>
#include <flight/modules/lib/Errors.hpp>

using namespace std;

struct RegistryValveInfo {
    SolenoidState state = SolenoidState::CLOSED;
    ActuationType actuation_type = ActuationType::NONE;
    ValvePriority actuation_priority = ValvePriority::NONE;
};

struct RegistrySensorInfo {
    double measured_value;
    double normalized_value;
    SensorStatus status;
};

class Registry {
public:
    Registry();

    /**
     * Load sensor data from global_config
     * Do not call if global_config has not been created yet
     */
    void initialize();

    struct {
        bool hard_abort = false;
        bool soft_abort = false;
        Stage stage = Stage::WAITING;
        double stage_status = 0;
        int stage_progress = 0;
        long mcl_start_time = 0;
    } general;

    struct {
        int status = 0;
        bool resetting = false;
        priority_queue<Packet, vector<Packet>, Packet::compareTo> ingest_queue; /* what type is this */
    } telemetry;

    // valve type --> valve location --> valve info
    map<string, map<string, RegistryValveInfo>> valves;

    map<string, map<string, RegistrySensorInfo>> sensors;
};

extern Registry global_registry;

/*
class Registry {
private:
    unordered_map<string, FieldBase *> fields;

    template <typename T>
    Field<T>* cast(FieldBase* base){

        Field<T>* field = dynamic_cast<Field<T>*>(base);

        if(field){
            return field;
        }
        throw DYNAMIC_CAST_ERROR();
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
*/

#endif //FLIGHT_REGISTRY_HPP

