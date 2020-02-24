#include <Wire.h>

#define SLAVE_ADDRESS 0x04
double thermo = 0.0;
double pressure = 0.0;
double load = 0.0;

void setup() {
  // put your setup code here, to run once:
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  thermo = random(1, 500) / 20.0;
  pressure = random(1, 500) / 20.0;
  load = random(1, 500) / 20.0;
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
  union cvt {
    float val;
    unsigned char byte_array[4];
  } x;
  x.val = thermo;
  
  union cvt2 {
    float val;
    unsigned char byte_array[4];
  } y;
  y.val = pressure;
  
  union cvt3 {
    float val;
    unsigned char byte_array[4];
  } z;
  z.val = load;

  byte data[12];
  for(int i = 0; i < 4; i++){ data[i] = x.byte_array[i];}
  for(int i = 4; i < 8; i++){ data[i] = y.byte_array[i - 4];}
  for(int i = 8; i < 12; i++){ data[i] = z.byte_array[i - 8];}
  
  Wire.write(data, 12);
}

