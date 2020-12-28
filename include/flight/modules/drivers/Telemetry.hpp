#ifndef FLIGHT_TELEMETRY_HPP
#define FLIGHT_TELEMETRY_HPP

#include <string>
#include <queue>
#include <cstdio>
#include <boost/array.hpp>
#include <boost/asio.hpp>
#include <unistd.h>
#include <mutex>
#include <thread>
#include <flight/modules/lib/Packet.hpp>

using namespace std;
using boost::asio::ip::tcp;

class Telemetry {
private:
    bool connection;
    queue<string> ingest_queue;

    // lockable object used to specify when things need exclusive access.
    mutex mtx;
    thread* recv_thread = nullptr;
    bool TERMINATE_FLAG = false;

    boost::asio::io_context io_context;
    tcp::socket socket = tcp::socket(io_context);

public:
    Telemetry();
    queue<string> read(int num_messages);
    bool write(const Packet& packet);
    void recv_loop();
    bool get_status() const;
    void reset();
    bool connect();
    void end();
};


#endif //FLIGHT_TELEMETRY_HPP
