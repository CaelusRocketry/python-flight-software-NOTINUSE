#include <Wire.h>
 
#define SLAVE_ADDRESS 0x08
 
// 10 byte data buffer
int receiveBuffer[9];
uint8_t keepCounted = 0;
 
 
// Read data in to buffer, offset in first element.
void receiveData(int byteCount){
  int counter = 0;
  while(Wire.available()) {
    receiveBuffer[counter] = Wire.read();
    //Serial.print("Got data: ");
    //Serial.println(receiveBuffer[counter]);
    counter ++;
  }
}
 
 
// Use the offset value to select a function
void sendData(){
  if (receiveBuffer[0] == 99) {
    writeData(keepCount());
  } else{
    Serial.println("No function for this address");
  }
}
 
 
// Write data
void writeData(char newData) {
  char data[] = {receiveBuffer[0], newData};
  int dataSize = sizeof(data);
  Wire.write(data, dataSize);
}
 
 
// Counter function
int keepCount() {
  keepCounted ++;
  if (keepCounted > 255) {
    keepCounted = 0;
    return 0;
  } else {
    return keepCounted;
  }
}
 
void setup(){
  Serial.begin(9600); // start serial for output
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.println("I2C Ready!");
}
 
void loop(){
  delay(100);
}
