#include "SensorArduino.hpp"

SensorArduino::SensorArduino() {
  pinMode(13, OUTPUT);
}

int SensorArduino::recvSerialByte(){
    while(!Serial.available()) {
			// Wait for something to be available from the serial
		}

    return Serial.read();
}

const int THERMOCOUPLE_TYPE = 0;
const int PRESSURE_TYPE = 1;

const int ALL_SENSORS_REGISTERED_SIGNAL = 255;

void SensorArduino::registerSensors() {
    // int num_sensors = recvSerialByte();
    // this->num_thermocouples = recvSerialByte();
    // this->num_pressures = recvSerialByte();

	// 	// Initialize arrays
    // this->thermocouples = new Thermocouple[num_thermocouples];
    // this->pressure_sensors = new PressureSensor[num_pressures];

	// // Keep track of how many we have added so far, so we can
	// // insert the sensors in their correct places in the arrays
	// int thermocouple_len = 0;
    // int pressure_len = 0;

	// 	// Loop until we have read num_sensors
    // for (int i = 0; i < num_sensors; i++) {
	// 	int sensor_type = recvSerialByte();

	// 	// Set the pinMode of this sensor's pin to INPUT
	// 	// Then, instantiate the PressureSensor
	// 	if (sensor_type == PRESSURE_TYPE) {
	// 		int pin = recvSerialByte();

	// 		pinMode(pin, INPUT);

	// 		// Store the value in the pressure_sensors array
	// 		this->pressure_sensors[pressure_len] = PressureSensor(pin);
	// 		pressure_len++;
	// 	}

	// 	// Read the pins for this sensor from Serial
	// 	// Then, instantiate the PressureSensor
	// 	// note: should these become input pins?
	// 	else if (sensor_type == THERMOCOUPLE_TYPE) {
	// 		int pins[4];

	// 		for(int i = 0; i < 4; i++) {
	// 			pins[i] = recvSerialByte();
	// 		}

	// 		// Store the value in the thermocouples array
	// 		this->thermocouples[thermocouple_len] = Thermocouple(pins);
	// 		thermocouple_len++;
	// 	}

	// 	// Signal an error through LED pin 13
	// 	else {
	// 		error();
	// 	}
    // }



	// temp fix: hardcode all values for the 1/23 nitrous cold flow test
	// NOTE: 0 THERMOCOUPLES ARE CODED FOR ATM SO FIX THIS LATER IF THERMOS ARE USED IN THE TEST

	int num_sensors = 4;
    this->num_thermocouples = 0;
    this->num_pressures = num_sensors;
	int thermocouple_len = 0;
    int pressure_len = 0;

	// Initialize arrays
    // this->thermocouples = new Thermocouple[num_thermocouples];
    this->pressure_sensors = new PressureSensor[num_pressures];

	int sensor_types[] = {PRESSURE_TYPE, PRESSURE_TYPE, PRESSURE_TYPE, PRESSURE_TYPE};
	int pressure_pins[] = {14, 15, 16, 17};
	int thermocouple_pins[8];

	// Loop until we have read num_sensors
    for (int i = 0; i < num_sensors; i++) {
		int sensor_type = sensor_types[i];

		// Set the pinMode of this sensor's pin to INPUT
		// Then, instantiate the PressureSensor
		if (sensor_type == PRESSURE_TYPE) {
			int pin = pressure_pins[i];

			pinMode(pin, INPUT);

			// Store the value in the pressure_sensors array
			this->pressure_sensors[pressure_len] = PressureSensor(pin);
			pressure_len++;
		}

		// Read the pins for this sensor from Serial
		// Then, instantiate the PressureSensor
		// note: should these become input pins?
		else if (sensor_type == THERMOCOUPLE_TYPE) {
			int pins[4];

			for(int i = thermocouple_len * 4; i < (thermocouple_len + 1) * 4; i++) {
				pins[i] = thermocouple_pins[i];
			}

			// Store the value in the thermocouples array
			this->thermocouples[thermocouple_len] = Thermocouple(pins);
			thermocouple_len++;
		}

		// Signal an error through LED pin 13
		else {
			error();
		}
    }

    this->registered = true;

    // Return signal saying that all the sensors were successfully registered
    Serial.write(ALL_SENSORS_REGISTERED_SIGNAL);
}

void SensorArduino::update() {
	// Cannot do anything if the sensors have not been registered
	// To register them, call SensorArduino::registerSensors()
	if(!this->registered) {
		return;
	}

	// Update temperatures for all thermocouples
	for(int i = 0; i < this->num_thermocouples; i++) {
		this->thermocouples[i].updateTemp();
	}

	// Update temperatures for all pressure sensors
	for(int i = 0; i < this->num_pressures; i++) {
		this->pressure_sensors[i].updatePressure();
	}
}

void SensorArduino::read() {
	// Send the temperature of the thermocouple
	// labeled by the first pin of the thermocouple
	for(int i = 0; i < this->num_thermocouples; i++) {
		this->sendData(
			this->thermocouples[i].pins[0],
			this->thermocouples[i].getTemp()
		);
	}

	// Send the pressure of the pressure sensor
	// labeled by the sensor's pin
	for(int i = 0; i < this->num_pressures; i++) {
		this->sendData(
			this->pressure_sensors[i].getPin(),
			this->pressure_sensors[i].getPressure()
		);
	}
}

void SensorArduino::sendData(int pin, float val) {
	// This Union helps us convert `val` to a byte array.
	union cvt {
		float val;
		unsigned char byte_array[4];
	} x;

	// `val` and `byte_array` are unified values
	// by assigning `val`, we can access its individual bytes
	// through `byte_array`
	x.val = val;

	// Writes [pin, bytes_of_val]
	Serial.write(pin);
	for(int i = 0; i < 4; i++){
		Serial.write(x.byte_array[i]);
	}
}

// Visual error for testing, turns LED on pin 13 on if there's an error
void SensorArduino::error() {
	digitalWrite(13, HIGH);
}

SensorArduino::~SensorArduino() {
	delete[] this->thermocouples;
	delete[] this->pressure_sensors;
}
