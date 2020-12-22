#include <assert.h>
#include <Logger/logger_util.h>
#include <flight/modules/tasks/TelemetryTask.hpp>
#include <flight/modules/drivers/Telemetry.hpp>
#include <boost/algorithm/string.hpp>
#include <flight/modules/lib/Util.hpp>

void TelemetryTask::initialize() {
    this->telemetry.connect();
}


void TelemetryTask::read(){
    log("Reading telemetry");
    bool status = this->telemetry.status();
    this->registry->put("telemetry.status", status);

    if (status) {
        log("Status was true");

        queue<string> packets = this->telemetry.read(-1);
        log("Read packet queue");

        //get the current ingest queue from the registry
        auto ingest_queue = this->registry->get<priority_queue<Packet, vector<Packet>, Packet::compareTo>>("telemetry.ingest_queue");
        log("Read ingest_queue");

        //for packet in packets read from telemetry, push packet to ingest queue
        for(string &packet_string = packets.front(); !packets.empty(); packets.pop()) {
            log("Packet: " + packet_string);
            // This line is broken because of Packet.cpp


            // strip of the "END"s off each packet_string string
            vector<string> split_packets = Util::split(packet_string, "END");

            for(auto packet : split_packets) {
                log("Packet to be decoded: " + packet);
                ingest_queue.push(Packet::fromString(packet));
            }
        }

        this->registry->put("telemetry.ingest_queue", ingest_queue);
    }

    log("here gets here");

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