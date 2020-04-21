#ifndef FLIGHT_FIELD_HPP
#define FLIGHT_FIELD_HPP

#include <flight/modules/mcl/FieldBase.hpp>

using namespace std;

template <class T>
class Field : public virtual FieldBase {
    private:
        const string _id;
        T _val;
        float _time;

    public:
        Field(const string &id)
        : _id(id),
          _time(-1) {}


        Field(const string &id, T val)
        : _id(id),
          _val(val),
          _time(-1) {}

        string getId(){ return _id; }

        T getVal(){ return _val; }

        float getTime() { return _time; }

        void setVal(T val){ _val = val; }
};

#endif //FLIGHT_FIELD_HPP
