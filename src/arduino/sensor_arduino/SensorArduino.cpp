#include <SensorArduino.hpp>

#define SLAVE_ADDRESS 0x04

float SensorArduino::getThermo() {
    auto thermo_ret = thermocouple.getTemp();

    if(thermo_ret.second) {
        Serial.println("There's a fault in the thermocouple");
    }

    return thermo_ret.first;
}

float SensorArduino::getPressure() {
    return pressure_sensor.getPressure();
}

void SensorArduino::receiveData() {
    
}

SensorArduino::SensorArduino() {
    // Sensor data variables
    thermo_val = 0.0;
    pressure_val = 0.0;
    load_val = 0.0;

    index = 0;

    // I2C initialization
    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    // Sensor initialization
    Serial.begin(9600);
}

void SensorArduino::read() {
    // put your main code here, to run repeatedly:
    thermo_val = getThermo();
    pressure_val = getPressure();
    load_val = random(1, 500) / 20.0;
    sensorVars current{thermo_val, pressure_val, load_val};
    buffer[index] = current;
    index += 1;

    sendData();
}

void SensorArduino::sendData(){
    Serial.print("Thermo: ");
    Serial.print(thermo_val);
    Serial.print(", Pressure: ");
    Serial.print(pressure_val);
    Serial.print(", Load: ");
    Serial.print(load_val);
    Serial.println();

    const int dataSize = index * 12;
    uint8_t data[dataSize];
    for(int j = 0; j < index; j++){
    sensorVars bufferedData = buffer[j];
    union cvt {
        float val;
        unsigned char byte_array[4];
    } x;
    x.val = bufferedData.thermo;
    
    union cvt2 {
        float val;
        unsigned char byte_array[4];
    } y;
    y.val = bufferedData.pressure;
    
    union cvt3 {
        float val;
        unsigned char byte_array[4];
    } z;
    z.val = bufferedData.load;
    
    int startIndex = j * 12; 
    for(int i = startIndex; i < startIndex + 4; i++){ data[i] = x.byte_array[i - startIndex];}
    for(int i = startIndex + 4; i < startIndex + 8; i++){ data[i] = y.byte_array[i - startIndex - 4];}
    for(int i = startIndex + 8; i < startIndex + 12; i++){ data[i] = z.byte_array[i - startIndex - 8];}
    }

    Wire.write(data, dataSize);
}
