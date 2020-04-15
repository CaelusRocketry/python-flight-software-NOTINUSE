#include <flight/modules/mcl/Registry.hpp>
#include <Logger/logger_util.h>

Registry::Registry(string name){
    this->name = name;
    log(this->name);
}