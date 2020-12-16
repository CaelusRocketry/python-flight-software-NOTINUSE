#ifndef FLIGHT_TELEMETRY_HPP
#define FLIGHT_TELEMETRY_HPP

#include <string>
#include <queue>
#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <mutex>
#include <thread>
#include <flight/modules/lib/Packet.hpp>

using namespace std;

class Telemetry {
private:

    string IP;
    int PORT;
    long int DELAY_LISTEN;
    long int DELAY_SEND;
    bool connection;
    queue<string> ingest_queue;
    queue<string> send_queue;

    // lockable object used to specify when things need exclusive access.
    mutex mtx;
    thread* recv_thread = nullptr;
    bool TERMINATE_FLAG = false;

    struct sockaddr_in serv_addr;
    int sock;


public:
    Telemetry();
    queue<string> read(int num_messages);
    bool write(Packet packet);
    void recv_loop();
    bool status();
    void reset();
    bool connect();
    void end();
};


#endif //FLIGHT_TELEMETRY_HPP
