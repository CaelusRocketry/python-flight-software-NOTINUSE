package sensors

import "time"

type MAX31856 struct {
	MAX31856 *MAX31856
}

func InitAmplifier() *MAX31856 {
	var spiClockSpeed int64 = 100000
	devPathCh0 := "/dev/spidev0.0"
	timeoutPeriod := time.Second

	sensor, err := MAX31856.Setup(devPathCh0, spiClockSpeed, timeoutPeriod)

	if err != nil {
		panic(err)
	}

	return sensor
}

// Temp returns temperature (C) for the thermocouple
func (m *MAX31856) Temp() float64 {
	temp, err := m.GetTempOnce()
	if err != nil {
		panic(err)
	}
	return temp
}
