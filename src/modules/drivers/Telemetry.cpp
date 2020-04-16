#include <queue>
#include <Logger/logger_util.h>
#include <flight/modules/drivers/Telemetry.hpp>

Telemetry::Telemetry(){
    log("Telemetry driver created");
    IP = "127.0.0.1";
    port = 5005;
}

string Telemetry::read(){
    return "Message";
}

void Telemetry::write(){

}