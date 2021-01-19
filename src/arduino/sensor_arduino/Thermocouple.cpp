#include "Thermocouple.hpp"

Thermocouple::Thermocouple(int *pins) {
	// Store the pin values
	// We copy these by value instead of by pointer to be safe
	this->pins = new int[4];

	for(int i = 0; i < 4; i++) {
		this->pins[i] = pins[i];
	}

	// Initialize the sensor
	this->maxthermo = new Adafruit_MAX31856(pins[0], pins[1], pins[2], pins[3]);

	// Begin making readings
	this->maxthermo->begin();
}

Thermocouple::~Thermocouple() {
	delete maxthermo;
	delete[] pins;
}

void Thermocouple::updateTemp() {
	// Read from the sensor
	float temperature = this->maxthermo->readThermocoupleTemperature();
	uint8_t fault = this->maxthermo->readFault();

	if (fault) {
		this->error(); // visual error
	} else {
		this->temperature = temperature;
	}
}

float Thermocouple::getTemp() {
	return this->temperature;
}

// Visual error for testing
void Thermocouple::error() {
	digitalWrite(13, HIGH);
}
