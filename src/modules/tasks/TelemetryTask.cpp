#include <Logger/logger_util.h>
#include <flight/modules/tasks/TelemetryTask.hpp>
#include <boost/algorithm/string.hpp>
#include <flight/modules/lib/Util.hpp>

void TelemetryTask::initialize() {
    this->telemetry.connect();
}

void TelemetryTask::read() {
    log("Reading telemetry");
    bool status = this->telemetry.get_status();
    global_registry.telemetry.status = status;

    if (status) {
        log("Status was true");

        queue<string> packets = this->telemetry.read(-1);
        log("Read packet queue");

        //for packet in packets read from telemetry, push packet to ingest queue
        for(string &packet_string_group = packets.front(); !packets.empty(); packets.pop()) {
            log("Packet: " + packet_string_group);
            // This line is broken because of Packet.cpp

            // strip of the "END"s off each packet_string_group string
            vector<string> split_packets = Util::split(packet_string_group, "END");
            for (auto packet_string : split_packets) {
                log("Packet to be decoded: " + packet_string);
                json packet_json = json::parse(packet_string);
                Packet packet;
                from_json(packet_json, packet);
                global_registry.telemetry.ingest_queue.push(packet);
            }
        }
    }
    log("here gets here");
}

void TelemetryTask::actuate(){
    log("Actuating telemetry");
    if (global_flag.telemetry.reset) {
        this->telemetry.reset();
    } else {
        enqueue();
        auto& send_queue = global_flag.telemetry.send_queue;

        // for each packet in the send_queue, write that packet to telemetry
        for (auto &packet = send_queue.top(); !send_queue.empty(); send_queue.pop()) {
            this->telemetry.write(packet);
        }
    }
}

void TelemetryTask::enqueue() {
    auto &enqueue_queue = global_flag.telemetry.enqueue;

    // for each packet in the enqueue_queue, push that packet to the send_queue
    for(auto &packet = enqueue_queue.top(); !enqueue_queue.empty(); enqueue_queue.pop()) {
        global_flag.telemetry.send_queue.push(packet);
    }
}