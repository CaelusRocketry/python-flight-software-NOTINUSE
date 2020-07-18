// Serial/I2C definitions. MAKE SURE CLOSE_VENT, OPEN_VENT, PULSE MATCH WHATEVER'S IN valve_task.py
#define DATA 0
#define NO_ACTUATION 1
#define CLOSE_VENT 2
#define OPEN_VENT 3
#define PULSE 4

#define OVERRIDE 0
#define OVERRIDE_UNDO 1

// Timing stuff
#define OPEN_CYCLE 4
#define OPEN_CYCLE_CLOSE 2
#define PULSE_TIME 1

#define MAX_SPECIAL_POWER 4000
#define RELIEF_WAIT_TIME 1000
#define PULSE_WAIT_TIME 500
