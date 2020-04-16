#ifndef FLIGHT_TELEMETRY_HPP
#define FLIGHT_TELEMETRY_HPP

#include <string>
#include <queue>
#include <websocketpp/config/asio_no_tls_client.hpp>
#include <websocketpp/client.hpp>

using namespace std;

class Telemetry {
private:

    typedef websocketpp::client<websocketpp::config::asio_client> client;
    typedef websocketpp::lib::lock_guard<websocketpp::lib::mutex> scoped_lock;
    typedef websocketpp::log::alevel alevel;

    string IP;
    int PORT;
    double DELAY_LISTEN;
    double DELAY_SEND;
    bool _connection;
    bool INGEST_LOCK;
    queue<string> ingest_queue;
    queue<string> send_queue;

    client m_client;
    websocketpp::connection_hdl m_hdl;
    websocketpp::lib::mutex m_lock;
    bool m_open;
    bool m_done;


public:
    Telemetry();
    void run(const std::string & uri);
    void on_open(websocketpp::connection_hdl);
    void on_close(websocketpp::connection_hdl);
    void on_fail(websocketpp::connection_hdl);
    void telemetry_loop();


};


#endif //FLIGHT_TELEMETRY_HPP
