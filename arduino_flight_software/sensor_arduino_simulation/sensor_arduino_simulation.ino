const int PRESSURE_SENSOR_RATING = 1000;

void setup() {
  // put your setup code here, to run once:
   Serial.begin(9600);
}
void loop() {
  // put your main code here, to run repeatedly:
  int sensorVal=analogRead(A1);
  Serial.print("Sensor Value: ");
  Serial.print(sensorVal);
  float voltage = (sensorVal*5.0)/1024.0;
  Serial.print("\tVolts: ");
  Serial.print(voltage);
  int conversion = PRESSURE_SENSOR_RATING / 20;
  float pressure_psi = ((float)voltage - 0.5) * conversion;
//  float pressure_pascal = (3.0*((float)voltage-0.47))*1000000.0;
//  float pressure_bar = pressure_pascal/10e5;
  Serial.print("\tChange in pressure = ");
  Serial.print(pressure_psi);
  Serial.print("psi");
  Serial.print("\tPressure = ");
  Serial.print(pressure_psi + 14.69);
  Serial.println("psi");
//  Serial.println(” bars”);
//  Serial.print(“Pressure = “);
  delay(100);
}
