/*
toggle - on/off/on switch
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

// Pin definitions - each toggle switch takes up 2 pins, the pulse pins take up one pin each
#define NITROGEN_FILL 4
#define ETHANOL_DRAIN 6
#define ETHANOL_VENT 8
#define ETHANOL_MPV 10
#define NO_FILL 12
#define NO_DRAIN 14
#define NO_VENT 16
#define NO_MPV 18
#define ETHANOL_VENT_PULSE 20
#define NO_VENT_PULSE 21
#define ABORT_PIN 22

// Valve arduino pin definitions - MAKE SURE THESE MATCH VALVE ARDUINO
#define VALVE_NITROGEN_FILL 2
#define VALVE_ETHANOL_DRAIN 3
#define VALVE_ETHANOL_VENT 4
#define VALVE_ETHANOL_MPV 5
#define VALVE_NO_FILL 6
#define VALVE_NO_DRAIN 7
#define VALVE_NO_VENT 8
#define VALVE_NO_MPV 9

// Pin order and actuation types
#define PULSE 4
