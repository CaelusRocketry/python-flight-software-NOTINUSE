#ifndef FLIGHT_PSEUDOARDUINO_HPP
#define FLIGHT_PSEUDOARDUINO_HPP

using namespace std;

// Parent class for PseudoSensor/PseudoValve

class PseudoArduino {
    public:
        PseudoArduino() = default;
        virtual unsigned char* read() = 0;
        virtual void write(unsigned char* msg) = 0;
};


#endif //FLIGHT_PSEUDOARDUINO_HPP
