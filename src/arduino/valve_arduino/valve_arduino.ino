#include <Servo.h>
#include <Wire.h>

#define SLAVE_ADDRESS 0x08
// Pin definitions
#define NITROGEN_FILL 2
#define ETHANOL_DRAIN 3
#define ETHANOL_VENT 4
#define ETHANOL_MPV 5
#define NO_FILL 6
#define NO_DRAIN 7
#define NO_VENT 8
#define NO_MPV 9

const PINS = {2, 3, 4, 5, 6, 7, 8, 9};
const NUM_PINS = 8;

// MAKE SURE THIS IS COPIED OVER FROM THE LAUNCH BOX ONE PROPERLY
#define DATA_NITROGEN_FILL 2
#define DATA_ETHANOL_DRAIN 3
#define DATA_ETHANOL_VENT 4
#define DATA_ETHANOL_VENT_PULSE 5
#define DATA_ETHANOL_MPV 6
#define DATA_NO_FILL 7
#define DATA_NO_DRAIN 8
#define DATA_NO_VENT 9
#define DATA_NO_VENT_PULSE 10
#define DATA_NO_MPV 11
#define ABORT 12
#define OVERRIDE 13
#define OVERRIDE_UNDO 14;


#define VENT_PULSE_PINS_LENGTH
int vent_pins[] = new int[VENT_PULSE_PINS_LENGTH];
for(int i = 0; i < VENT_PULSE_PINS_LENGTH; i++){
  vent_pins[i] = -1;
}
vent_pins[DATA_NITROGEN_FILL] = NITROGEN_FILL;
vent_pins[DATA_ETHANOL_DRAIN] = ETHANOL_DRAIN;
vent_pins[DATA_ETHANOL_VENT] = ETHANOL_VENT;
vent_pins[DATA_ETHANOL_MPV] = ETHANOL_MPV;
vent_pins[DATA_NO_FILL] = NO_FILL;
vent_pins[DATA_NO_DRAIN] = NO_DRAIN;
vent_pins[DATA_NO_VENT] = NO_VENT;
vent_pins[DATA_NO_VENT_PULSE] = NO_MPV;

int pulse_pins[] = new int[VENT_PULSE_PINS_LENGTH];
for(int i = 0; i < VENT_PULSE_PINS_LENGTH; i++){
  pulse_pins[i] = -1;
}
pulse_pins[DATA_ETHANOL_VENT_PULSE] = ETHANOL_VENT;
pulse_pins[DATA_NO_VENT_PULSE] = NO_VENT;

const OPEN_CYCLE = 4;
const OPEN_CYCLE_CLOSE = 2;
const PULSE_TIME = 1;

boolean override = false;
boolean aborted = false;

// Ignore 0 and 1 in this
#define NUM_STATES 10
int states[] = new int[NUM_STATES];
unsigned long times[] = new unsigned long[NUM_STATES];
for(int i = 0; i < NUM_STATES; i++){
  times[i] = -1;
  states[i] = 0;
}

void setup() {
  // put your setup code here, to run once:
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.begin(9600);
  for(int i = 0; i < NUM_PINS; i++){
    pinMode(PINS[i], OUTPUT);
  }
}

void loop() {
  // Valve open cycle and also pulse control
  for(int i = 0; i < NUM_STATES; i++){
    if(times[i] == -1){
      continue;
    }
    if(millis() > times[i]){
      if(states[i] == 2){
        states[i] = 0;
        times[i] = -1;
      }
      else if(states[i] == 1){
        states[i] = 0;
        times[i] = millis() + OPEN_CYCLE_CLOSE;
      }
      else if(states[i] == 0){
        states[i] = 1;
        times[i] = millis() + OPEN_CYCLE;
      }
      else{
        error();
      }
    }
  }
  launchBox();
  pi();
}

void error(){
  digitalWrite(13, HIGH);
}

void close(int pin){
  digitalWrite(pin, LOW);
  states[i] = 0;
  times[i] = -1;
}

void open(int pin){
  digitalWrite(pin, HIGH);
  states[i] = 1;
  times[i] = millis() + OPEN_CYCLE;
}

void pulse(int pin){
  states[i] = 2;
  times[i] = millis() + PULSE_TIME;
}

void abort(){
  for(int i = 0; i < NUM_PINS; i++){
    close(PINS[i]);
  }
  aborted = true;
}


void launchBox(){
  while(Serial.available() > 0){
    int incoming = Serial.read();
    ingestLaunchbox(incoming);
  }
}

void ingestLaunchbox(int incoming){
  if(incoming == OVERRIDE){
    override = true;
    return;
  }
  if(incoming == OVERRIDE_UNDO){
    override = false;
    return;
  }
  if(incoming == ABORT){
    abort();
    return;
  }
  if(!override){
    return;
  }
  if(incoming < VENT_PULSE_PINS_LENGTH){
    else if(vent_pins[incoming] != -1){
      open(vent_pins[incoming]);
    }
    else if(pulse_pins[incoming] != -1){
      pulse(pulse_pins[incoming]);
    }
    else{
      error();
    }
    return;
  }
  if(incoming - 32 > 0 && incoming - 32 < VENT_PULSE_PINS_LENGTH){
    if(vent_pins[incoming - 32] != -1){
      close(vent_pins[incoming - 32]);
    }
    else{
      error();
    }
  }
  error();
}

void pi(){

}

void receiveData(){
  if(override){
    return;
  }
}

void sendData(){

}

