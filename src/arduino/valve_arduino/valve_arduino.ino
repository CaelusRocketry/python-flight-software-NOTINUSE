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


// MAKE SURE THIS MATCHES config.json order
const VALVE_ORDER = {NITROGEN_FILL, ETHANOL_DRAIN, ETHANOL_VENT, ETHANOL_MPV, NO_FILL, NO_DRAIN, NO_VENT, NO_MPV};

// Pin counts. MAKE SURE the order in ALL_PINS matches config.json.
#define NUM_VALVES 8;
const ALL_PINS = {NITROGEN_FILL,
                  ETHANOL_DRAIN,
                  ETHANOL_VENT,
                  ETHANOL_MPV,
                  NO_FILL,
                  NO_DRAIN,
                  NO_VENT,
                  NO_MPV};
const MAX_PIN = 10;
int states[] = new int[MAX_PIN];
unsigned long times[] = new unsigned long[MAX_PIN];

// Serial/I2C definitions. MAKE SURE CLOSE_VENT, OPEN_VENT, PULSE MATCH WHATEVER'S IN valve_task.py
const DATA = 0;
const CLOSE_VENT = 1;
const OPEN_VENT = 2;
const PULSE = 3;
const OVERRIDE = 0;
const OVERRIDE_UNDO = 1;

// Timing stuff
const OPEN_CYCLE = 4;
const OPEN_CYCLE_CLOSE = 2;
const PULSE_TIME = 1;

boolean override = false;

void setup() {
  // put your setup code here, to run once:
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.begin(9600);
  for(int i = 0; i < NUM_VALVES; i++){
    pinMode(ALL_PINS[i], OUTPUT);
  }
  for(int i = 0; i < MAX_PIN; i++){
    times[i] = -1;
    states[i] = CLOSE_VENT;
  }
  pinMode(13, OUTPUT);
}

void loop() {
  // Valve open cycle control and pulse control
  for(int i = 0; i < NUM_STATES; i++){
    if(times[i] == -1){
      continue;
    }
    if(millis() > times[i]){
      if(states[i] == PULSE){
        close(i);
      }
      else if(states[i] == OPEN_VENT){
        close(i);
        times[i] = millis() + OPEN_CYCLE_CLOSE;
      }
      else if(states[i] == CLOSE_VENT){
        open(i);
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
  states[i] = CLOSE_VENT;
  times[i] = -1;
}

void open(int pin){
  digitalWrite(pin, HIGH);
  states[i] = OPEN_VENT;
  times[i] = millis() + OPEN_CYCLE;
}

void pulse(int pin){
  open(pin);
  states[i] = PULSE;
  times[i] = millis() + PULSE_TIME;
}

void launchBox(){
  while(Serial.available() > 0){
    int cmd = Serial.read();
    int data = Serial.read();
    ingestLaunchbox(cmd, data);
  }
}

void ingestLaunchbox(int cmd, int data){
  if(cmd == DATA){
    if(data == OVERRIDE){
      override = true;
    }
    else if(data == OVERRIDE_UNDO){
      override = false;
    }
    else{
      error();
    }
    return;
  }
  if(!override){
    return;
  }
  switch(cmd){
    case CLOSE_VENT:
      close(data);
      break;
    case OPEN_VENT:
      open(data);
      break;
    case PULSE:
      pulse(data);
      break;
    default:
      error();
      break;
  }
}

void actuate(int loc_idx, int actuation_idx){
  int valve_pin = VALVE_ORDER[loc_idx];
  switch(actuation_idx){
    case 0:
      // Pulse
      pulse(valve_pin);
      break;
    case 1:
      // Open vent
      open(valve_pin);
      break;
    case 2:
      // Close vent
      close(valve_pin);
      break;
    case 3:
      // None
      //TODO: Implement this
      break;
    default:
      error();
      break;
  }

}

void receiveData(int byteCount){
  while(Wire.available()){
    int loc_idx = Wire.read();
    int actuation_type = Wire.read();
    if(override){
      return;
    }
    int valve_pin = ALL_PINS[loc_idx];
    switch(actuation_type){
      case CLOSE_VENT:
        close(valve_pin);
        break;
      case OPEN_VENT:
        open(valve_pin);
        break;
      case PULSE:
        pulse(valve_pin);
        break;
    }
  }
}

void sendData(){
  unsigned long data = 0;
  if(override){
    data = 1;
  }
  for(int valve = 0; valve < NUM_VALVES; valve++){
    int state = states[ALL_PINS[valve]];
    data = data | (state << (valve * 2 + 1))
  }
  byte buf[4];
  buf[0] = (byte) data;
  buf[1] = (byte) data >> 8;
  buf[2] = (byte) data >> 16;
  buf[3] = (byte) data >> 24;
  Wire.write(buf, 4);
}
