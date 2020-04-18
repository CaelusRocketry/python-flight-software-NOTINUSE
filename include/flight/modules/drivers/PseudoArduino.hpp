#ifndef FLIGHT_PSEUDOARDUINO_HPP
#define FLIGHT_PSEUDOARDUINO_HPP

using namespace std;

class PseudoArduino {
private:
public:
//    virtual PseudoArduino() {};
    PseudoArduino() {};
    virtual char* read() = 0;
    virtual void write(char* msg) = 0;
};


#endif //FLIGHT_PSEUDOARDUINO_HPP
