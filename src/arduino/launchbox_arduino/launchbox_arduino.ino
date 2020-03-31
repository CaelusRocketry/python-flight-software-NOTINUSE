/*
toggle - on/off switch
pulse - you push it and it opens, waits .05s, and closes

Nitrogen Fill (1 switch (toggle)))
Ethanol Drain (1 switch (toggle))
Ethanol Vent (1 button (pulse), 1 switch (toggle))
Ethanol Main Propellant Valve (1 switch (toggle))

Nitrous Oxide Fill
Nitrous Oxide Drain
Nitrous Oxide Vent
Nitrous Oxide Main Propellant Valve
*/

// Pin definitions
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

// Valve arduino pin definitions - MAKE SURE THESE MATCH VALVE ARDUINO
#define VALVE_NITROGEN_FILL 2
#define VALVE_ETHANOL_DRAIN 3
#define VALVE_ETHANOL_VENT 4
#define VALVE_ETHANOL_MPV 5
#define VALVE_NO_FILL 6
#define VALVE_NO_DRAIN 7
#define VALVE_NO_VENT 8
#define VALVE_NO_MPV 9

// Serial definitions
const DATA = 0;
const CLOSE_VENT = 1;
const OPEN_VENT = 2;
const PULSE = 3;
const OVERRIDE = 0;
const OVERRIDE_UNDO = 1;

// Pin order and actuation types
const MAX_PIN = 14;
int PIN_MAP[] = new int[MAX_PIN];
PIN_MAP[NITROGEN_FILL] = VALVE_NITROGEN_FILL;
PIN_MAP[ETHANOL_DRAIN] = VALVE_ETHANOL_DRAIN;
PIN_MAP[ETHANOL_VENT] = VALVE_ETHANOL_VENT;
PIN_MAP[ETHANOL_VENT_PULSE] = VALVE_ETHANOL_VENT;
PIN_MAP[ETHANOL_MPV] = VALVE_ETHANOL_MPV;
PIN_MAP[NO_FILL] = VALVE_NO_FILL;
PIN_MAP[NO_DRAIN] = VALVE_NO_DRAIN;
PIN_MAP[NO_VENT] = VALVE_NO_VENT;
PIN_MAP[NO_VENT_PULSE] = VALVE_NO_VENT;
PIN_MAP[NO_MPV] = VALVE_NO_MPV;

// Pin counts
const NUM_VALVES = 8;
const NUM_BUTTONS = 2;

// Local variables
boolean override;
boolean aborted;

// Arrays that keep track of stuff
// States: 0 means closed, 1 means open -> should match digitalRead
// TODO: CHECK IF digitalRead CAN BE COMPARED TO A BOOLEAN
boolean states[] = new boolean[NUM_VALVES];
boolean pulsing[] = new boolean[NUM_BUTTONS];
int vent_pins[] = new int[NUM_VALVES];
int pulse_pins[] = new int[NUM_BUTTONS];

void setup(){
    for(int i = 2; i <= 13; i++){
        pinMode(i, INPUT);
    }
    Serial.begin(9600);
    override = false;
    aborted = false;

    vent_pins[] = {NITROGEN_FILL, ETHANOL_DRAIN, ETHANOL_VENT, ETHANOL_MPV, NO_FILL, NO_DRAIN, NO_VENT, NO_MPV};
    pulse_pins[] = {ETHANOL_VENT_PULSE, NO_VENT_PULSE};
    for(int i = 0; i < NUM_VALVES; i++){
        states[i] = 0;
    }
    for(int i = 0; i < NUM_BUTTONS; i++){
        pulsing[i] = false;
    }
}

void loop(){
    if(aborted){
        return;
    }
    for(int i = 0; i < NUM_VALVES; i++){
        if(digitalRead(vent_pins[i]) != states[i]){
            states[i] = !states[i];
            if(states[i]){
                send_message(OPEN_VENT, PIN_MAP[vent_pins[i]]);
            }
            else{
                send_message(CLOSE_VENT, closed[i]);
            }
        }
    }
    if(digitalRead(OVERRIDE_PIN) && !override){
        override = true;
        send_message(DATA, OVERRIDE);
    }
    if(!digitalRead(OVERRIDE_PIN) && override){
        override = false;
        send_message(DATA, OVERRIDE_UNDO);
    }
    if(digitalRead(ABORT_PIN)){
        aborted = true;
        send_message(DATA, OVERRIDE);
        for(int i = 0; i < NUM_VALVES; i++){
            send_message(CLOSE_VENT, PIN_MAP[vent_pins[i]]);
        }
    }
    for(int i = 0; i < NUM_BUTTONS; i++){
        if(digitalRead(pulse_pins[i])){
            if(pulsing[i]){
                continue;
            }
            pulsing[i] = true;
            send_message(PULSE, PIN_MAP[pulse_pins[i]]);
        }
        else{
            pulsing[i] = false;
        }
    }
}

void send_message(int cmd, int data){
    if(!override){
        return;
    }
    Serial.write(cmd);
    Serial.write(data);
    delay(50);
}