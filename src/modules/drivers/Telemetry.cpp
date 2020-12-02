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
    queue<string> q;
    for(int i = 0; i < num_messages; i++){
        q.push(ingest_queue.front());
        ingest_queue.pop();
    }
    mtx.unlock();
    return q;
}


bool Telemetry::write(Packet packet){
    string msg = packet.toString();
    log("Sending: " + msg);
    send(sock, msg.c_str(), msg.length(), 0);
    this_thread::sleep_for(chrono::milliseconds(DELAY_SEND));
    return true;
}

void Telemetry::recv_loop(){
    while(connection){
        if(TERMINATE_FLAG){
            break;
        }
        try{
            // Read in data from socket
            char buffer[1024] = {0};
            ::read(sock, buffer, 1024);
            string msg(buffer);
            mtx.lock();
            ingest_queue.push(msg);
            mtx.unlock();
            log("Received: " + msg);
            this_thread::sleep_for(chrono::seconds(DELAY_LISTEN));
        }
        catch (...){
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
    sock = 0;
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        connection = false;
        throw SOCKET_CREATION_ERROR();
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    if(inet_pton(AF_INET, IP.c_str(), &serv_addr.sin_addr)<=0)
    {
        connection = false;
        throw INVALID_ADDRESS_ERROR();
    }

    if (::connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        connection = false;
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
    //TODO: Kill the socket connection
    connection = false;
    sock = 0;
}
