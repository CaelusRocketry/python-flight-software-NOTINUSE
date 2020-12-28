#include <chrono>
#include <Logger/logger_util.h>
#include <flight/modules/drivers/Telemetry.hpp>
#include <flight/modules/mcl/Config.hpp>
#include <flight/modules/lib/Errors.hpp>

using boost::asio::ip::address;

Telemetry::Telemetry() {
    // Initialize variables
    connection = false;
}

queue<string> Telemetry::read(int num_messages) {
    mtx.lock(); // prevents anything else from a different thread from accessing the ingest_queue until we're done
    if (num_messages > ingest_queue.size() || num_messages == -1){
        num_messages = ingest_queue.size();
    }

    // type of list where elements are exclusively inserted from one side and removed from the other.
    queue<string> q;
    for (int i = 0; i < num_messages; i++){
        q.push(ingest_queue.front());
        ingest_queue.pop();
    }

    mtx.unlock();
    return q;
}

// This sends the packet to the GUI!
bool Telemetry::write(const Packet& packet) {
    // Convert to JSON and then to a string
    json packet_json;
    to_json(packet_json, packet);

    // Note: add "END" at the end of the packet, so packets are split correctly
    string packet_string = packet_json.dump() + "END";
    log("Telemetry: Sending packet: " + packet_string);
    boost::system::error_code error;
    boost::asio::write(socket, boost::asio::buffer(packet_string), boost::asio::transfer_all(), error);

    if (error) {
        throw boost::system::system_error(error);
    }

    this_thread::sleep_for(chrono::milliseconds(global_config.telemetry.DELAY));
    return true;
}

// This gets called in the main thread
void Telemetry::recv_loop() {
    while (connection && !TERMINATE_FLAG) {
        try {
            // Read in data from socket
            boost::array<char, 1024> buf;
            boost::system::error_code error;
            socket.read_some(boost::asio::buffer(buf), error);

            if (error == boost::asio::error::eof) {
                end();
                break; // Connection closed cleanly by peer.
            } else if (error) {
                throw boost::system::system_error(error); // Some other error.
            }

            string msg(buf.data());

            mtx.lock();
            ingest_queue.push(msg);
            mtx.unlock();

            log("Telemetry: Received: " + msg);
            this_thread::sleep_for(chrono::seconds(global_config.telemetry.DELAY));
        }
        catch (std::exception& e){
            log(e.what());
            end();
            throw SOCKET_READ_ERROR();
        }
    }
}

bool Telemetry::get_status() const {
    return connection;
}

void Telemetry::reset() {
    end();
    if(!connect()){
        end();
    }
}

bool Telemetry::connect() {
    try {
        log("Telemetry: Connecting");
        socket.open(boost::asio::ip::tcp::v4());

        address ip_address = address::from_string(global_config.telemetry.GS_IP);
        boost::asio::ip::tcp::endpoint ep(ip_address, global_config.telemetry.GS_PORT);

        log("Telemetry: Connecting Socket");
        socket.connect(ep);

        log("Telemetry: Connected!");
    } catch(std::exception& e) {
        log(e.what());
        throw SOCKET_CONNECTION_ERROR();
    }

    thread t(&Telemetry::recv_loop, this);
    connection = true;
    TERMINATE_FLAG = false;
    recv_thread = &t;
    recv_thread->detach();

    return true;
}

void Telemetry::end() {
    TERMINATE_FLAG = true;
    socket.close();
    connection = false;
}
