#include <Adafruit_MAX31856.h>
#include <Wire.h>

#define SLAVE_ADDRESS 0x04
#define MAX_PRESSURE 1000
#define ROOM_PRESSURE 15

// Sensor objects
Adafruit_MAX31856 maxthermo = Adafruit_MAX31856(10, 11, 12, 13);
const int pressurePin = A1;

// Sensor data variables
double thermo = 0.0;
double pressure = 0.0;
double load = 0.0;

// Contains all three data variables
struct sensorVars {
  double thermo;
  double pressure;
  double load;
};

// Temporary data storage
sensorVars buffer[1000]{};
int index = 0;

void setup() {
  // I2C initialization
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  // Sensor initialization
  maxthermo.begin();
  pinMode(pressurePin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  thermo = getThermo();
  pressure = getPressure();
  load = random(1, 500) / 20.0;
  sensorVars current{thermo, pressure, load};
  buffer[index] = current;
  index += 1;
}

float mapVal(float val, float lower1, float upper1, float lower2, float upper2){
  float diff1 = upper1 - lower1;
  float diff2 = upper2 - lower2;
  float factor = diff2 / diff1;
  return (val - lower1) * factor + lower2;
}

float getThermo(){
  float temp = maxthermo.readThermocoupleTemperature();
  uint8_t fault = maxthermo.readFault();
  if(fault){
    Serial.println("There's a fault in the thermocouple");
  }
  return temp;
}

float getPressure(){
  float analog = analogRead(pressurePin);
  Serial.println(analog);
  float voltage = mapVal(analog, 0, 1023, 0, 5);
  Serial.println(voltage);
  float pressure = mapVal(voltage, 0.5, 4.5, 0, MAX_PRESSURE);
  Serial.println(pressure);
  Serial.println();
  return pressure + ROOM_PRESSURE;
}

void receiveData(){
  
}

void sendData(){
  Serial.print("Thermo: ");
  Serial.print(thermo);
  Serial.print(", Pressure: ");
  Serial.print(pressure);
  Serial.print(", Load: ");
  Serial.print(load);
  Serial.println();

  const int dataSize = index * 12;
  byte data[dataSize];
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

