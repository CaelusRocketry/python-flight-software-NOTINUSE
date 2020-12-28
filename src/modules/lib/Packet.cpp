#include <flight/modules/lib/Packet.hpp>
#include <flight/modules/lib/Util.hpp>

using nlohmann::json;

void to_json(json& j, const Packet& packet) {
    j = json{
        {"logs", packet.logs},
        {"level", packet.level},
        {"timestamp", packet.timestamp}
    };
}

void from_json(const json& j, Packet& packet) {
    // First, get timestamp and log priority
    long timestamp = j.at("timestamp").get<long>();
    auto priority = static_cast<LogPriority>(j.at("priority").get<int>());
    packet = Packet(priority, timestamp);

    // Then, add logs
    j.at("logs").get_to(packet.logs); // overloaded in Log.hpp
}

void Packet::add(const Log& log) {
    logs.push_back(log);
}

vector<Log> Packet::getLogs() {
    return this->logs;
}
