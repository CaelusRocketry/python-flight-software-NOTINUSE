#include <flight/modules/mcl/Flag.hpp>

// Adds all flag fields from config and general default fields

void Flag::enqueue(const Log& log, LogPriority logPriority) {
    Packet packet(logPriority);
    packet.add(log);
    telemetry.enqueue.push(packet);
}

void Flag::log_info(const string &header, const string &message) {
    enqueue(Log(header, message), LogPriority::INFO);
}

void Flag::log_debug(const string &header, const string &message) {
    enqueue(Log(header, message), LogPriority::DEBUG);
}

void Flag::log_warning(const string &header, const string &message) {
    enqueue(Log(header, message), LogPriority::WARN);
}

void Flag::log_critical(const string &header, const string &message) {
    enqueue(Log(header, message), LogPriority::CRIT);
}

// Define the value declared with extern in the header file
Flag global_flag;

/*

Flag::Flag(){
    log("Flag created");

    //general fields
    add<bool>("general.progress", false);

    //telemetry fields
    add<priority_queue<Packet, vector<Packet>, Packet::compareTo>>("telemetry.enqueue");
    add<priority_queue<Packet, vector<Packet>, Packet::compareTo>>("telemetry.send_queue");
    add<bool>("telemetry.reset", true);

    // Valve fields
    for(string outer : Util::parse_json({"valves", "list"})) {  // [solenoid]
        for(string inner : Util::parse_json_list({"valves", "list", outer})) {  // ["pressure_relief", "propellant_vent", "main_propellant_valve"]
            add<SolenoidState>("valve." + outer + "." + inner, SolenoidState::CLOSED);
            add<ActuationType>("valve_actuation_type." + outer + "." + inner, ActuationType::NONE);
            add<ValvePriority>("valve_actuation_priority." + outer + "." + inner, ValvePriority::NONE);
        }
    }
}

 */

