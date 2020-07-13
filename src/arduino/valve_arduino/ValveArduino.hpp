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
#define NUM_VALVES 8;

class ValveArduino {
  private:
    // MAKE SURE THIS MATCHES config.json order
    const VALVE_ORDER;

    // Pin counts. MAKE SURE the order in ALL_PINS matches config.json.
    const ALL_PINS;
    const MAX_PIN;
    int states[];
    bool actuation_on[];
    unsigned long times[];

    // Serial/I2C definitions. MAKE SURE CLOSE_VENT, OPEN_VENT, PULSE MATCH WHATEVER'S IN valve_task.py
    const DATA;
    const NO_ACTUATION;
    const CLOSE_VENT;
    const OPEN_VENT;
    const PULSE;
    const OVERRIDE;
    const OVERRIDE_UNDO;

    // Timing stuff
    const OPEN_CYCLE;
    const OPEN_CYCLE_CLOSE;
    const PULSE_TIME;

    bool override;

    void error();
    void close(int pin);
    void open(int pin);
    void pulse(int pin);
    void ingestLaunchbox(int cmd, int data);

  public:
    ValveArduino::ValveArduino();
    void read();
    void receiveData(int byteCount){;
    void sendData();
    void launchBox();
    void actuate(int loc_idx, int actuation_idx);
}
