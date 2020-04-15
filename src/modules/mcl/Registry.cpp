#include <flight/modules/mcl/Registry.hpp>
#include <flight/modules/mcl/Field.hpp>
#include <Logger/logger_util.h>

Registry::Registry(){
    log("Registry created");
    Field<int>* f = new Field<int>("hello", 5);
    log(f->getName());
    log(to_string(f->getVal()));
    f->setVal(10);
    log(to_string(f->getVal()));
}

void Registry::get(string name){
    log("Getting");
}

void Registry::put(string name){
    log("Putting");
}