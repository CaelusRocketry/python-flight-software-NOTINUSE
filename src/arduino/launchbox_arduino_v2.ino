#define NITROGEN_FILL 2
#define ETHANOL_DRAIN 3
#define ETHANOL_VENT 4
#define ETHANOL_VENT_PULSE 5
#define ETHANOL_MPV 6
#define NO_FILL 7
#define NO_DRAIN 8
#define NO_VENT 9
#define NO_VENT_PULSE 10
#define NO_MPV 11
#define ABORT_PIN 12
#define OVERRIDE_PIN 13

// Serial definitions
const int DATA = 0;
const int CLOSE_VENT = 1;
const int OPEN_VENT = 2;
const int PULSE = 3;
const int OVERRIDE = 0;
const int OVERRIDE_UNDO = 1;

// Local variables
boolean override = false;
boolean aborted = false;

int switchPins[] = {NITROGEN_FILL, ETHANOL_DRAIN, ETHANOL_VENT, ETHANOL_MPV, NO_FILL, NO_DRAIN, NO_VENT, NO_MPV};
int pulsePins[] = {ETHANOL_VENT_PULSE, NO_VENT_PULSE};
  
void setup() {
  for (int i = 2; i <= 13; i++) {
    pinMode(i, INPUT);
  }
  Serial.begin(9600);
}

void loop() {
  if (aborted) {
    return;
  }
  for (int i = 0; i < 8; i++){
    if(digitalRead(switchPins[i]) == HIGH){
      send_message(OPEN_VENT, switchPins[i]);
    }
    if(digitalRead(switchPins[i]) == LOW){
      send_message(CLOSE_VENT, switchPins[i]);
    }
  }

  if(digitalRead(OVERRIDE_PIN) == HIGH && !override){
      override = true;
      send_message(DATA, OVERRIDE);
  }

  if(digitalRead(OVERRIDE_PIN) == LOW && override){
      override = false;
      send_message(DATA, OVERRIDE_UNDO);
  }

  if(digitalRead(ABORT_PIN) == HIGH){
      aborted = true;
      send_message(DATA, OVERRIDE);
      for(int i = 0; i < 8; i++){
          send_message(OPEN_VENT, switchPins[i]);
      }
  }
  
  for(int i = 0; i < 2; i++){
    if(digitalRead(pulsePins[i]) == HIGH){
      send_message(PULSE, pulsePins[i]);
    }
  }
}

void send_message(int cmd, int data) {
    if(!override){
        return;
    }
    Serial.write(cmd);
    Serial.write(data);
    delay(50);
}