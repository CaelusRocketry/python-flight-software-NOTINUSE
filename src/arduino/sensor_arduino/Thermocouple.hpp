#include "Arduino.h"
#include <Adafruit_MAX31856.h>

#ifndef THERMOCOUPLE_HPP
#define THERMOCOUPLE_HPP

class Thermocouple {
	private:
		/**
		 * The Adafruit sensor
		 */
		Adafruit_MAX31856 *maxthermo;

		/**
		 * The internal temperature storage
		 */
		float temperature = 0;
	public:
		int *pins;
		
		/**
		 * Empty constructor.
		 * !!! THIS DOES NOT INSTANTIATE ANYTHING. AT ALL.
		 */
		Thermocouple() {};

		/**
		 * Initializes the sensor given a 4-int long array of pins
		 */
		Thermocouple(int *pins);

		/**
		 * Release the memory for the Adafruit sensor and the pins
		 */
		~Thermocouple();

		/**
		 * Reads the temperature from the sensor. If there is a fault, create a
		 * visual error at LED 13. Otherwise, store the temperature in this->temperature.
		 * The value of this->temperature can be accessed via Thermocouple::getTemp().
		 */
		void updateTemp();

		/**
		 * Get the temperature [float]
		 */
		float getTemp();

		/**
		 * Visual error for testing
		 */
		void error();
};

#endif