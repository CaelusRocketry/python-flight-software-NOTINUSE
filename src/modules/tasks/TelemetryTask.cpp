#include <assert.h>
#include <Logger/logger_util.h>
#include <flight/modules/tasks/TelemetryTask.hpp>
#include <flight/modules/drivers/Telemetry.hpp>
#include <boost/algorithm/string.hpp>

void TelemetryTask::initialize() {
    this->telemetry.connect();
}


void TelemetryTask::read(){
    auto status = this->telemetry.status();
    this->registry->put("telemetry.status", status);

    if(status) {
        auto packets = this->telemetry.read(-1);

        //get the current ingest queue from the registry
        auto ingest_queue = this->registry->get<priority_queue<Packet, vector<Packet>, Packet::compareTo>>("telemetry.ingest_queue");

        //for packet in packets read from telemetry, push packet to ingest queue
        for(auto &packet = packets.front(); !packets.empty(); packets.pop()) {
            log("Packet: " + packet);
            // This line is broken because of Packet.cpp

            // strip of the "END"s off each packet string
            vector<string> split_packets;
            boost::split(split_packets, packet, boost::is_any_of("END"));

            for(auto pack : split_packets) {
                ingest_queue.push(Packet::fromString(pack));
            }
        }

        this->registry->put("telemetry.ingest_queue", ingest_queue);
    }

}

void TelemetryTask::actuate(){
    log("Actuating telemetry");
    auto reset = this->flag->get<bool>("telemetry.reset");
    if(reset) {
        this->telemetry.reset();
    }
    else {
        enqueue();
        auto send_queue = this->flag->get<priority_queue<Packet, vector<Packet>, Packet::compareTo>>("telemetry.send_queue");

        // for each packet in the send_queue, write that packet to telemetry
        for(auto &packet = send_queue.top(); !send_queue.empty(); send_queue.pop()) {
            this->telemetry.write(packet);
        }

        this->flag->put("telemetry.send_queue", priority_queue<Packet, vector<Packet>, Packet::compareTo>());
    }
}

void TelemetryTask::enqueue() {
    auto send_queue = this->flag->get<priority_queue<Packet, vector<Packet>, Packet::compareTo>>("telemetry.send_queue");
    auto enqueue_queue = this->flag->get<priority_queue<Packet, vector<Packet>, Packet::compareTo>>("telemetry.enqueue");

    // for each packet in the enqueue_queue, push that packet to the send_queue
    for(auto &packet = enqueue_queue.top(); !enqueue_queue.empty(); enqueue_queue.pop()) {
        send_queue.push(packet);
    }

    this->flag->put("telemetry.enqueue", priority_queue<Packet, vector<Packet>, Packet::compareTo>());
    this->flag->put("telemetry.send_queue", send_queue);
}