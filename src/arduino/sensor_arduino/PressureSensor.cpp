#include "PressureSensor.hpp"

/**
 * Takes a value within a range and maps it to a value within another range.
 * @param x The value to map
 * @param in_min The lower boundary of the input range
 * @param in_max The upper boundary of the input range
 * @param out_min The lower boundary of the output range
 * @param out_max The upper boundary of the output range
 */
float map_value(float x, float in_min, float in_max, float out_min, float out_max) {
	float in_width = in_max - in_min;
	float out_width = out_max - out_min;
	float factor = out_width / in_width;
	return (x - in_min) * factor + out_min;
}

/**
 * Reads voltage and pressure values to this -> pressure.
 */
void PressureSensor::updatePressure() {
	// Read a value from this sensor's pin
	float pwmVal = analogRead(this -> pin);

	/* Old code (should be removed?)
	float voltage = map_val(pwmVal, 0, 1023, 0, 5);
	float base_pressure = map_val(voltage, 0.5, 4.5, 0, MAX_PRESSURE);
	pressure = base_pressure + ROOM_PRESSURE;
	*/

	// Maps a voltage value previously from 0-1024 to 0-5.
	// Someone pls fill in what the 0.01 does here
	float voltage = map_value(pwmVal, 0, 1024, 0, 5) + 0.0100;

	// Maps a pressure value previously from MIN_VOLTAGE-MAX_VOLTAGE to MIN_PSI-MAX_PSI.
	float psi = map_value(voltage, MIN_VOLTAGE, MAX_VOLTAGE, MIN_PSI, MAX_PSI);
	this->pressure = psi - MIN_PSI;
}

/**
 * @return uint8 containing the pin
 */
int PressureSensor::getPin(){
    return this->pin;
}

/**
 * @return float containing the most recent pressure reading
 */
float PressureSensor::getPressure(){
    return this->pressure;
}
