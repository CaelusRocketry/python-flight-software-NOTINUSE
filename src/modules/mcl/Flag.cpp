#include <flight/modules/mcl/Flag.hpp>

// Adds all flag fields from config and general default fields

void Flag::enqueue(const Log& log, LogPriority logPriority) {
    Packet packet(logPriority);
    packet.add(log);
    telemetry.enqueue.push(packet);
}

void Flag::log_info(const string &header, const json &message) {
    enqueue(Log(header, message), LogPriority::INFO);
}

void Flag::log_debug(const string &header, const json &message) {
    enqueue(Log(header, message), LogPriority::DEBUG);
}

void Flag::log_warning(const string &header, const json &message) {
    enqueue(Log(header, message), LogPriority::WARN);
}

void Flag::log_critical(const string &header, const json &message) {
    enqueue(Log(header, message), LogPriority::CRIT);
}

// Define the value declared with extern in the header file
Flag global_flag;
