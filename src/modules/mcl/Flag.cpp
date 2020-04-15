#include "flight/modules/mcl/Flag.hpp"
#include <Logger/logger_util.h>

Flag::Flag(string name){
    this->name = name;
    log(this->name);
}