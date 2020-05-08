#include <assert.h>
#include <Logger/logger_util.h>
#include <flight/modules/tasks/TelemetryTask.hpp>
#include <flight/modules/drivers/Telemetry.hpp>

void TelemetryTask::initialize() {
    this->telemetry.connect();
}


void TelemetryTask::read(){
    log("Reading telemetry");
    auto status = this->telemetry.status();
    this->registry->put("telemetry.status", status);

    if(status) {
        auto packets = this->telemetry.read(-1);
        auto ingest_queue = this->registry->get<priority_queue<Packet, vector<Packet>, Packet::compareTo>>("telemetry.ingest_queue");
        for(auto &packet = packets.front(); !packets.empty(); packets.pop()) {
            ingest_queue.push(Packet::fromString(packet));
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

        for(auto &packet = send_queue.top(); !send_queue.empty(); send_queue.pop()) {
            this->telemetry.write(packet);
        }

        this->flag->put("telemetry.send_queue", priority_queue<Packet, vector<Packet>, Packet::compareTo>());
    }
}

void TelemetryTask::enqueue() {
    auto send_queue = this->flag->get<priority_queue<Packet, vector<Packet>, Packet::compareTo>>("telemetry.send_queue");
    auto enqueue_queue = this->flag->get<priority_queue<Packet, vector<Packet>, Packet::compareTo>>("telemetry.enqueue");

    for(auto &packet = enqueue_queue.top(); !enqueue_queue.empty(); enqueue_queue.pop()) {
        send_queue.push(packet);
    }

    this->flag->put("telemetry.enqueue", priority_queue<Packet, vector<Packet>, Packet::compareTo>());
    this->flag->put("telemetry.send_queue", send_queue);
}