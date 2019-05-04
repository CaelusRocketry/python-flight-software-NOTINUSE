package sensors

import (
	"github.com/kpeu3i/bno055"
)

type Sensor bno055.Sensor
type Vector bno055.Vector

func InitIMU() *Sensor {
	sensor, err := bno055.NewSensor(0x28, 1)
	if err != nil {
		panic(err)
	}

	err = sensor.UseExternalCrystal(true)
	if err != nil {
		panic(err)
	}

	axisConfig, err := sensor.AxisConfig()
	if err != nil {
		panic(err)
	}

	return sensor
}

// Acc returns a vector with acceleration data
func (s *Sensor) Acc() Vector {
	v, err := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v
}

// AccX returns acceleration data for x
func (s *Sensor) AccX() float64 {
	v := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v.X
}

// AccY returns acceleration data for x
func (s *Sensor) AccY() float64 {
	v := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v.Y
}

// AccZ returns acceleration data for x
func (s *Sensor) AccZ() float64 {
	v := s.Accelerometer()
	if err != nil {
		panic(err)
	}
	return v.Z
}

// Gyro returns a vector with gyro data
func (s *Sensor) Gyro() Vector {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v
}

// GyroX returns pitch
func (s *Sensor) GyroX() float64 {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v.X
}

// GyroY returns roll
func (s *Sensor) GyroY() float64 {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v.Y
}

// GyroZ returns yaw
func (s *Sensor) GyroZ() float64 {
	v, err := s.Gyroscope()
	if err != nil {
		panic(err)
	}
	return v.Z
}
