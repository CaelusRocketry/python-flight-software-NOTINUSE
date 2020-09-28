// Serial definitions. MAKE SURE CLOSE_VENT, OPEN_VENT, PULSE MATCH WHATEVER'S IN valve_task.py
#define SEND_DATA_CMD 255
#define ACTUATE_CMD 254
#define REGISTERED_CONFIRMATION 253

#define NO_ACTUATION 1
#define CLOSE_VENT 2
#define OPEN_VENT 3
#define PULSE 4

// Launchbox definitions
#define L_DO_NOTHING 1
#define L_OPEN_VENT 2
#define L_CLOSE_VENT 3
#define L_PULSE 4

// Timing stuff
#define OPEN_CYCLE 4
#define OPEN_CYCLE_CLOSE 2
#define PULSE_TIME 1

#define MAX_SPECIAL_POWER 3000
#define RELIEF_WAIT_TIME 1000
#define PULSE_WAIT_TIME 500
