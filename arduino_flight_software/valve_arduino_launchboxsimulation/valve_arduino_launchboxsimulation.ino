void setup() {
  // put your setup code here, to run once:
  pinMode(7, OUTPUT);
  pinMode(6, INPUT);
  pinMode(5, INPUT);
  Serial.begin(9600);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if (digitalRead(6)){
    Serial.println("Button 1 on");
    if(digitalRead(5)) {
        Serial.println("Button 2 on");
        digitalWrite(7, HIGH);
        delay(500);
      }
    else {
        Serial.println("Button 2 off");
        digitalWrite(7, LOW);
        delay(500);
      }
  }
  else{
    digitalWrite(7, HIGH);
    Serial.println("LED on");
    delay(1000);
    digitalWrite(7, LOW);
    Serial.println("LED off");
    delay(1000);
  }
}
