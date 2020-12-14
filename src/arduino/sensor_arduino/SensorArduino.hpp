#include "Arduino.h"
#include "Thermocouple.hpp"
#include "PressureSensor.hpp"
#include <stdint.h>

// Include guard
#ifndef SENSOR_ARDUINO_HPP
#define SENSOR_ARDUINO_HPP

class SensorArduino {
	private:
		int num_thermocouples;

		/**
		 * Map each thermocouple to the four pins that define it
		 */
		Thermocouple *thermocouples;
		
		/**
		 * 
		 */
		int num_pressures;

		/**
		 * Specifies the delay, in ms, between each time we send data to the Pi
		 */
		const int SEND_DELAY = 50;

		/**
		 * Blocks until something can be read from the serial.
		 * @return A single integer representing to most recently-read value.
		 */
		int recvSerialByte();

		/**
		 * Flag so we know if the sensors are registered
		 */
		bool registered = false;

	public:
		/**
		 * Sets pin 13 to an output pin
		 */
		SensorArduino();

		/**
		 * Destructor method. delete[]s the thermocouple and pressure sensor values.
		 */
		~SensorArduino();

		// Why is this public?
		/**
		 * Map each pressure sensor to the pin that defines it
		 */
		PressureSensor *pressure_sensors;

		/**
		 * Register the sensors for this arduino.
		 * TODO: make sure that the format matches what the pi is sending
		 * Format:
		 * 	1 int: num_sensors
		 *  1 int: num_thermocouples
		 * 	1 int: num_pressures
		 * 
		 * For next num_sensors readings:
		 *  1 int: sensor type
		 * 		0 if thermocouple
		 * 			--> Read 4 ints: the pins of the thermocouple
		 * 		1 if pressure
		 * 			--> Read 1 int: the pin of the pressure sensor
		 * 
		 * Example: 5, 2, 3, 1, 1, 1, 2, 1, 3, 0, 4, 5, 6, 7, 0, 8, 9, 10, 11
		 * [5] sensors total
		 * [2] are thermocouples
		 * [3] are pressure sensors
		 * 
		 * [1, 1] = Pressure sensor at pin 1
		 * [1, 2] = Pressure sensor at pin 2
		 * [1, 3] = Pressure sensor at pin 3
		 * 
		 * [0, 4, 5, 6, 7] = Thermocouple at pins 4, 5, 6, and 7
		 * [0, 8, 9, 10, 11] = Thermocouple at pins 8, 9, 10, and 11
		 */
		void registerSensors();

		/**
		 * Iterates over the thermocouples and reads their data.
		 * Sends the data to Serial, labelled by the first pin of the thermocouple.
		 * Iterates over the pressure sensors and reads their data.
		 * Sends the data to Serial, labelled by the pin of the pressure sensor.
		 */
		void read();

		/**
		 * If the SensorArduino has registered its sensors, update all of them.
		 * First, updates the temperatures of the thermocouples in the order
		 * they were registered in.
		 * Second, updates the pressures of the pressure sensors in the order
		 * they were registered in.
		 */
		void update();

		/**
		 * Sends a value to a pin by writing to the serial.
		 * Writing format:
		 * 	1 byte: The pin
		 * 	4 bytes: The individual bytes of `val`
		 * 
		 * @param pin The pin to send data to [int]
		 * @param val The value to send [float]
		 */
		void sendData(int pin, float val);

		/**
		 * Visual error for testing, turns LED on pin 13 on if there's an error
		 */
		void error();
};

#endif