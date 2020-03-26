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
#define NITROGEN_FILL_SWITCH 2
#define ETHANOL_DRAIN_SWITCH 3
#define ETHANOL_VENT_SWITCH 4
#define ETHANOL_VENT_BUTTON 5
#define ETHANOL_MPV 6
#define NO_FILL_SWITCH 7
#define NO_DRAIN_SWITCH 8
#define NO_VENT_SWITCH 9
#define NO_VENT_BUTTON 10
#define NO_MPV 11
#define ABORT 12
#define OVERRIDE 13


void setup(){
    for(int i = 2; i <= 13; i++){
        pinMode(i, INPUT);
    }
}

void loop(){
    String msg = get_message();
}

void send_message(){

}

String get_message(){

}