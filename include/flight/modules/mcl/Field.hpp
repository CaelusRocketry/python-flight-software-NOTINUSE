#ifndef FLIGHT_FIELD_HPP
#define FLIGHT_FIELD_HPP

using namespace std;

template <typename T>
class Field {
    private:
        const string _name;
        T _val;

    public:
        Field(const string &name, int val)
        : _name(name),
          _val(val) {}

        string getName(){return _name;}

        T getVal(){return _val;}

        void setVal(T val){_val = val;}
};

#endif //FLIGHT_FIELD_HPP
