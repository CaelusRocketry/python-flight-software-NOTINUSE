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
#define ABORT 12
#define OVERRIDE 13

// Pin counts
#define NUM_VALVES 8;
#define NUM_BUTTONS 2;

// Serial message variables
const OVERRIDE_UNDO = 14;
int open[] = new int[NUM_VALVES];
int closed[] = new int[NUM_VALVES];

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
        open[i] = vent_pins[i];
        closed[i] = vent_pins[i] + 32; // Remember that this is +32
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
                send_message(open[i]);
            }
            else{
                send_message(closed[i]);
            }
        }
    }
    if(digitalRead(OVERRIDE) != override){
        override = !override;
        if(override){
            send_message(OVERRIDE);
        }
        else{
            send_message(OVERRIDE_UNDO);
        }
    }
    if(digitalRead(ABORT)){
        aborted = true;
        send_message(ABORT);
    }
    for(int i = 0; i < NUM_BUTTONS; i++){
        if(digitalRead(pulse_pins[i])){
            if(pulsing[i]){
                continue;
            }
            pulsing[i] = true;
            send_message(pulse_pins[i]);
        }
        else{
            pulsing[i] = false;
        }
    }
}

void send_message(int msg){
    if(!override){
        return;
    }
    Serial.write(msg);
}