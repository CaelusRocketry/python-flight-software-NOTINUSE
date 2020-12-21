#include <chrono>
#include <Logger/logger_util.h>
#include <flight/modules/drivers/Telemetry.hpp>
#include <flight/modules/lib/Util.hpp>
#include <flight/modules/lib/Errors.hpp>

Telemetry::Telemetry(){
    IP = Util::parse_json_value({"telemetry", "GS_IP"});
    PORT = stoi(Util::parse_json_value({"telemetry", "GS_PORT"}));
    DELAY_LISTEN = stoi(Util::parse_json_value({"telemetry", "DELAY_LISTEN"}));
    DELAY_SEND = stoi(Util::parse_json_value({"telemetry", "DELAY_SEND"}));

    // Initialize variables
    connection = false;
}

queue<string> Telemetry::read(int num_messages){
    mtx.lock(); // prevents anything else from a different thread from accessing the ingest_queue until we're done
    if(num_messages > ingest_queue.size() || num_messages == -1){
        num_messages = ingest_queue.size();
    }

    // type of list where elements are exclusively inserted from one side and removed from the other.
    queue<string> q;
    for(int i = 0; i < num_messages; i++){
        q.push(ingest_queue.front());
        ingest_queue.pop();
    }
    mtx.unlock();
    return q;
}

// This sends the packet to the GUI!
bool Telemetry::write(Packet packet){
    string msg = packet.toString();
    log("Sending: " + msg);
    boost::system::error_code error;
    boost::asio::write(socket, boost::asio::buffer(msg), boost::asio::transfer_all(), error);

    if(error) {
        throw boost::system::system_error(error);
    }

    this_thread::sleep_for(chrono::milliseconds(DELAY_SEND));
    return true;
}

// This gets called in the main thread
void Telemetry::recv_loop(){
    while(connection){
        if(TERMINATE_FLAG){
            break;
        }
        try {
            // Read in data from socket
            boost::array<char, 1024> buf;
            boost::system::error_code error;
            size_t len = socket.read_some(boost::asio::buffer(buf), error);

            if (error == boost::asio::error::eof) {
                end();
                break; // Connection closed cleanly by peer.
            }
            else if (error)
                throw boost::system::system_error(error); // Some other error.

            string msg(buf.data());
            mtx.lock();
            ingest_queue.push(msg);
            mtx.unlock();
            log("Received: " + msg);
            this_thread::sleep_for(chrono::seconds(DELAY_LISTEN));
        }
        catch (std::exception& e){
            log(e.what());
            end();
            throw SOCKET_READ_ERROR();
        }
    }
}

bool Telemetry::status(){
    return connection;
}

void Telemetry::reset(){
    end();
    if(!connect()){
        end();
    }
}

bool Telemetry::connect(){
    try {
        socket.open(boost::asio::ip::tcp::v4());

        boost::asio::ip::address ip_address = boost::asio::ip::address::from_string(IP);
        boost::asio::ip::tcp::endpoint ep(ip_address, PORT);

        socket.bind(ep);
        socket.connect(ep);
    }
    catch(std::exception& e) {
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

void Telemetry::end(){
    TERMINATE_FLAG = true;
    socket.close();
    connection = false;
}
