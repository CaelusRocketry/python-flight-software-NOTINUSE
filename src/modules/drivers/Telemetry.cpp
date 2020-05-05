#include <chrono>
#include <Logger/logger_util.h>
#include <flight/modules/drivers/Telemetry.hpp>
#include <flight/modules/lib/Util.hpp>

Telemetry::Telemetry(){
    IP = Util::parse_json_value({"telemetry", "GS_IP"});
    PORT = stoi(Util::parse_json_value({"telemetry", "GS_PORT"}));
    DELAY_LISTEN = stoi(Util::parse_json_value({"telemetry", "DELAY_LISTEN"}));
    DELAY_SEND = stoi(Util::parse_json_value({"telemetry", "DELAY_SEND"}));

    // Initialize variables
    connection = false;
}

queue<string> Telemetry::read(int num_messages){
    mtx.lock();
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


bool Telemetry::write(string msg){
    log("Sending: " + msg);
    send(sock, msg.c_str(), msg.length(), 0);
    this_thread::sleep_for(chrono::milliseconds(DELAY_SEND));
    return true;
}

void Telemetry::recv_loop(){
    while(connection){
        if(TERMINATE_FLAG){
            return;
        }
        try{
            // Read in data from socket
            char buffer[1024] = {0};
            int valread = ::read(sock, buffer, 1024);
            string msg(buffer);
            mtx.lock();
            ingest_queue.push(msg);
            mtx.unlock();
            log("Received: " + msg);
            this_thread::sleep_for(chrono::seconds(DELAY_LISTEN));
        }
        catch (...){
            log("Encountered exception, terminating socket");
            end();
            return;
        }
    }
    return;
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
        printf("\n Socket creation error \n");
        connection = false;
        return false;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    if(inet_pton(AF_INET, IP.c_str(), &serv_addr.sin_addr)<=0)
    {
        printf("\nInvalid address/ Address not supported \n");
        connection = false;
        return false;
    }

    if (::connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("\nConnection Failed \n");
        connection = false;
        return false;
    }

    thread t(&Telemetry::recv_loop, this);
    recv_thread = &t;

    connection = true;
    return true;
}

void Telemetry::end(){
    TERMINATE_FLAG = true;
    recv_thread->join();
    //TODO: Kill the socket connection
    connection = false;
    sock = 0;
    TERMINATE_FLAG = false;
}
